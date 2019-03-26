#!/usr/bin/env python
# coding: UTF-8


##################################################
# 情報入力(客先側)
##################################################
def input_info_list_sample(csvdata_1row):
    """
    #サンプル社の必要な情報の取得、加工を行う
    """
    date_str = csvdata_1row[0]  # 日付
    status_str = csvdata_1row[1]  # 出社又は休暇
    time_start_str = csvdata_1row[2]  # 出社時刻
    time_end_str = csvdata_1row[3]  # 勤務終了時間
    return (date_str, status_str, time_start_str, time_end_str)  # タプル追加を返す


def input_info_list_sample2(csvdata_1row):
    pass  # 処理なし
    return ("", "", "", "")  # タプル追加を返す


##################################################
# メインのクラス
##################################################
class StructInfoForCSVCmp:
    """
    情報の取得、加工、比較を実行
    """

    # クラス変数
    # チェックIDに対応する関数を辞書に格納
    ID2FunctionDir = {
        "sample": input_info_list_sample,
        "client2": input_info_list_sample2,
    }

    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, filename, checkIDStr0):
        self.filename = filename
        self.info_tuplelist_pri = []
        self.info_tuplelist_client = []

        self.checkIDStr = checkIDStr0  # チェックID

        self.cmp_result_ind_list = []  # 個別の比較結果
        self.cmp_result_flag = False  # 比較結果問題無しなら1

    ##################################################
    # 情報入力1(自社側)
    ##################################################
    def input_info_list_pri(self, csvdata_1row):
        """
        自社側の必要な情報の取得、加工を行う
        """
        date_str = csvdata_1row[0]  # 日付
        status_str = csvdata_1row[1]  # 出社又は休暇
        time_start_str = csvdata_1row[2]  # 出社時刻
        time_end_str = csvdata_1row[3]  # 勤務終了時間
        self.info_tuplelist_pri.append(
            (date_str, status_str, time_start_str, time_end_str)
        )  # タプル追加

    ##################################################
    # 情報入力2
    # 客先の種類によって動作を切り替える
    ##################################################
    def input_info_list_client(self, csvdata_1row):
        """
        客先側の必要な情報の取得、加工を行う
        """
        no_target_frag = False  # 対象となっていない客先ならば1を返す

        # チェックIDに応じた関数を取得
        try:
            check_function = StructInfoForCSVCmp.ID2FunctionDir[self.checkIDStr]
            # チェックIDに応じた関数を実行
            resultTupple = check_function(csvdata_1row)
            self.info_tuplelist_client.append(resultTupple)  # タプル追加
        except Exception as e:
            no_target_frag = True
            print("{}に対応する関数を実行できませんでした\n", self.checkIDStr)
            print(e, "error occurred")
        return no_target_frag

    ##################################################
    # 比較を行う
    ##################################################
    def cmp_info_list(self):
        """
        比較を行う
        """
        for info_tuple_pri, info_tuple_client1 in zip(
            self.info_tuplelist_pri, self.info_tuplelist_client
        ):
            # 1行ごとの比較結果を格納
            self.cmp_result_ind_list.append(info_tuple_pri == info_tuple_client1)

        # 総合的な比較結果を格納
        if len(self.cmp_result_ind_list) == 0:
            self.cmp_result_flag = False
        else:
            self.cmp_result_flag = all(self.cmp_result_ind_list)  # 全てtrueならtrue
