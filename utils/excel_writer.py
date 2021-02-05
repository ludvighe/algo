"""
Export dataframe to xlsx

"""

import numpy as np
import pandas as pd
import math
import xlsxwriter


# Define what column letter to assign based on index of column in df
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def column_lettering(i):
    if i >= len(alphabet):
        depth = math.floor(i / len(alphabet))
        return alphabet[depth - 1] + column_lettering(i - len(alphabet) * depth)
    return alphabet[i]


def df_to_excel(df, file_name, sheet_name='', background_color='#ffffff', font_color='#000000', column_size=18, dynamic_column_size=True):
    if sheet_name == '':
        sheet_name = file_name

    writer = pd.ExcelWriter(f'{file_name}.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name, index=False)

    # Column format definitions
    string_format = writer.book.add_format(
        {
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    dollar_format = writer.book.add_format(
        {
            'num_format': '$0.00',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    integer_format = writer.book.add_format(
        {
            'num_format': '0',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    # Get formatting for column
    def column_formatting(column_name='', column_data=''):
        # Static return. Could be made dynamic based on args.
        return string_format

    # Assign column formatting to sheet
    for i in range(len(df.columns)):
        letter = column_lettering(i)
        # print(f'Formatting cells: i={i}    letter={letter}   column={df.columns[i]}')

        final_column_size = column_size
        if dynamic_column_size and len(df.columns[i]) > column_size:
            final_column_size = len(df.columns[i])

        writer.sheets[sheet_name].set_column(
            f'{letter}:{letter}', final_column_size, string_format
        )

    writer.save()
