# Aloha
import dbf
import pandas as pd


class AlohaPOSDbf:

    def __init__(self):

        self.codepage = 'cp1251'  

    def read_dbf(self, log_name: str, dbf_path: str, dbf_name: str):

        """
        Open Aloha POS main dicts and shifts dbf-tables and convert to corresponding pandas dataframe;
        With logging to separate log-file (log_name: str). Awaits appropriate dbf-table names.
        Aloha POS dicts tables: 'CAT.DBF', 'CIT.DBF', 'ITM.DBF', 'RSN.DBF', 'TDR.DBF', 'CMP.DBF';
        Aloha POS shifts tables: 'GNDITEM.DBF', 'GNDTNDR.DBF', 'GNDVOID.DBF'.
        """

        try:
            file = f"{dbf_path}/{dbf_name}"
            table = dbf.Table(file, codepage=self.codepage)

        except Exception as Argument:
            with open(log_name, "a") as log_file:
                log_file.write(f"{self.now}: DBF READ ERROR: {dbf_name}, {str(Argument)}\n")

        else:
            with table.open(dbf.READ_ONLY):
                df = pd.DataFrame(table)

                if not df.empty:
                    if dbf_name == 'CAT.DBF':  # items sales categories dict table

                        # res: [0: category_id, 3: categ_name, 6: sales_categ ('Y' / 'N')]
                        l = [[item[0], item[3].rstrip()] for item in df.values.tolist() if item[6] == 'Y']

                    if dbf_name == 'CIT.DBF':  # items to sales categories links dict table
                        # res: [0: category_id, 2: item_id]
                        l = [[item[0], item[2]] for item in df.values.tolist()]

                    if dbf_name == 'ITM.DBF':  # items dict table

                        # res: [0: item_id, 5: item_longname, 37: item_price]
                        l = [[item[0], item[5].rstrip(), item[37]] for item in df.values.tolist()]

                    if dbf_name == 'RSN.DBF':  # item delete reasons dict table

                        # res: [0: reason_id, 3: reason_name]
                        l = [[item[0], item[3].rstrip()] for item in df.values.tolist()]

                    if dbf_name == 'TDR.DBF':  # currencies dict table

                        # res: [0: currency_id, 3: currency_name]
                        l = [[item[0], item[3].rstrip()] for item in df.values.tolist() if item[9] == 0]

                    if dbf_name == 'CMP.DBF':  # discounts / markups dict table

                        # res: [0: discount_id, 4: discount_name, 14: discount_rate]
                        l = [[item[0], item[4].rstrip()] for item in df.values.tolist() if item[14] == 1.0]

                    if dbf_name == 'GNDITEM.DBF':  # items(goods) expenditure(shift) table

                        # res: [2: check_id, 3: item_id, 5: category_id, 15: price, 18: date, 23: qnt, 25: disc_price]
                        l = [[item[2], item[18], item[3], item[23], item[15], item[25], item[5]] for item in
                             df.values.tolist()]  # if item[15] >= 0

                    if dbf_name == 'GNDTNDR.DBF':  # items(goods) expenditure(shift) table by payments

                        # res: [1: check_id, 4: payment_id, 5: pay_typeid]
                        l = [[item[1], item[4], item[5]] for item in df.values.tolist() if item[4] != 11]

                    if dbf_name == 'GNDVOID.DBF' and not df.empty: # items(goods) removed from sales by delete reasons

                        # res: [2: check_id, 4:item_id, 5: price, 6: date, 10: reason_id]
                        l = [[item[2], item[6], item[4], item[5], item[10]] for item in df.values.tolist()]

                    result_list = [list(map(lambda x: x, group)) for group in l]

                    return result_list
                else:
                    return []





