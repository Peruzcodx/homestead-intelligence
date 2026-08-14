import sqlite3
import pandas as pd


DB_PATH = "database/estatepulse.db"


def load_properties():

    connection = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            title,
            price,
            street,
            city,
            state,
            zip,
            neighborhood,
            bedrooms,
            bathrooms,
            sqft,
            property_type,
            availability,
            url
        FROM properties
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


def clean_data(df):

    df = df.copy()

    # Numeric columns
    numeric_columns = [
        "price",
        "bedrooms",
        "bathrooms",
        "sqft",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Text cleanup
    text_columns = [
        "title",
        "street",
        "city",
        "state",
        "zip",
        "neighborhood",
        "property_type",
        "availability",
        "url",
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    return df


def get_properties():

    df = load_properties()

    df = clean_data(df)

    return df
