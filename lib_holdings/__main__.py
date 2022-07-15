import glob, os, traceback
import click
import pandas as pd
from lib_holdings.api import ApiSession


@click.command()
@click.option("--start", default=0, type=int, help="Position of OCN to start with.")
@click.argument('infile_ocns', required=True, type=click.Path(exists=True))
@click.argument('infile_symb', required=True, type=click.Path(exists=True))
@click.argument('out_folder', required=True)
@click.option("--key", prompt="Your OCLC API key", help="OCLC API key.", hide_input=False)
@click.option("--secret", prompt="Your OCLC API secret", help="OCLC API secret.", hide_input=False)
def main(**kwargs):
    # create output folder (if it does not exist already)
    if not os.path.exists(kwargs.get('out_folder')):
        os.makedirs(kwargs.get('out_folder'), exist_ok=True)
    ocns = list(pd.read_csv(kwargs.get('infile_ocns'), header=None).iloc[:, 0].unique())
    symbols = list(pd.read_csv(kwargs.get('infile_symb'), header=None).iloc[:, 0].unique())
    session = ApiSession(kwargs.get('key'), kwargs.get('secret'))
    # break up into smaller batches
    n = 100
    error = False
    # store temporary files here:
    if not os.path.exists(f'{kwargs.get("out_folder")}/temp'):
        os.makedirs(f'{kwargs.get("out_folder")}/temp')
    for i in range(kwargs.get('start'), len(ocns), n):
        try:
            click.echo(f'fetch data for batch {i}-{i+n}')
            ocns_sub = ocns[i:i+n]
            holdings = aggregate(transform_holdings(session.extract_holdings(ocns_sub, symbols)))
            record_types = transform_records(session.extract_record_type(ocns_sub))
            holdings_with_type = holdings.merge(record_types, how='left')
            # store temporary batch
            holdings_with_type.to_csv(f'{kwargs.get("out_folder")}/temp/{i}-{i+n}.csv', index=False)
        except Exception as e:
            click.echo(traceback.format_exc())
            click.echo(f'{e}\n{e.__class__}\nerror in batch {i}-{i+n}.\ntry again with start = {i}')
            error = True
            break
    # merge the sub-batches
    if not error:
        table_big = pd.DataFrame()
        for file in glob.glob(f'{kwargs.get("out_folder")}/temp/*.csv'):
            table_big = pd.concat([table_big, pd.read_csv(file)])
            os.remove(file)  # then remove the temporary file
        table_big.to_csv(f'{kwargs.get("out_folder")}/holdings.csv', index=False)


def transform_holdings(data):
    to_df = []
    for symbol in data:
        for item in data[symbol]:
            holding = item['briefRecords'][0]['institutionHolding']
            to_df.append({'symbol': symbol, 'ocn': item['briefRecords'][0]['oclcNumber'],
                          'holdings': holding['totalHoldingCount']})
    return pd.json_normalize(to_df)


def transform_records(records):
    record_types = []
    for ocn in records:
        if len(records[ocn]) > 0:
            record_types.append({'ocn': ocn, 'recordType': records[ocn][0]['recordType']})
            # the multiple entries are holdings
    return pd.json_normalize(record_types)


def aggregate(df):
    agg = df.groupby('ocn').agg(sum_holdings=('holdings', 'sum')).reset_index()
    agg['ocn'] = agg['ocn'].astype(int)  # reset_index returns object type
    return agg


if __name__ == "__main__":
    main()
