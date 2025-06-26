import sqlite3 
import pandas as pd
import logging

from ingestion_db import ingest_db
import time

logging.basicConfig(
    filename= "logs/get_vendorSummary.log",
    level= logging.DEBUG,
    format= "%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a"
)

def createVendorSummary(conn):
    ''' function will merge the different tables to get the overall vendor summary and add new columns in resultant data'''
    vendorSalesSummary = pd.read_sql_query("""WITH FreightSummary AS (
        SELECT 
            VendorNumber,
            SUM(Freight) AS  FreightCost
            FROM vendor_invoice
            GROUP BY VendorNumber
        ),
    PurchaseSummary AS(
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM (p.Quantity) AS TotalPurchaseQuantity,
            SUM (p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
    ),

    SalesSummary AS (
        SELECT 
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) as TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM Sales
        GROUP BY VendorNo, Brand
)

    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.brand = ss.Brand
    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber  = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC""" , conn)
    return vendorSalesSummary


def clean_data(df):
    ''' function cleans the data and add additional insightful columns'''
    df['Volume'] = df['Volume'].astype('float') # consistent data type float

    # Treat missing values
    df.fillna(0, inplace = True)

    # Strip off empty spaces
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    # Create additional columns for auxilliary insights
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df[ 'ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars'])*100
    df['StockTurnover'] = df['TotalSalesQuantity']/df['TotalPurchaseQuantity']
    df['SalestoPurchaseRatio'] = df['TotalSalesDollars']/df['TotalPurchaseDollars']

    return df

if __name__ == '__main__':
    start = time.time()
    conn = sqlite3.connect('inventory.db')
    conn.execute("DROP TABLE IF EXISTS vendorSalesSummary;")
    conn.commit()


    logging.info('Creating Vendor Summary Table...')
    summary_df= createVendorSummary(conn)
    logging.info(summary_df.head())

    logging.info('Cleaning Data and making addition changes...')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting Data...')
    ingest_db(clean_df, 'vendorSalesSummary', conn)
    logging.info('Completed')
    
    end = time.time()
    totalTime = (end-start) / 60 
    print(f"Total Time Elapsed : {totalTime} minutes")
    conn.close()
