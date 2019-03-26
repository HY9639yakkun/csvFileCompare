#!/usr/bin/env python
# coding: UTF-8

import os  # フォルダ操作
import csv  # csv操作
import traceback  # エラー情報

from StructInfoForCSVCmp import StructInfoForCSVCmp as info_obj  # 情報格納オブジェクト


class ClassGetCSVInfo:
    """
    csvファイルから情報を取得するオブジェクトクラス
    情報格納オブジェクト「StructInfoForCSVCmp」を格納したリストと辞書を作成する

    コンストラクタ入力:
        input_path1:自社側フォルダのパス
        input_path2:客先側フォルダのパス
        input_client_type:比較方法
    """

    # コンストラクタ
    def __init__(self, input_path1, input_path2, input_client_type):
        self.dir_path_pri = input_path1  # 格納フォルダのパス
        self.dir_path_client = input_path2  # 格納フォルダのパス
        self.client_type = input_client_type  # 客先の種別

        # 情報格納オブジェクトを格納するリスト
        self.info_obj_list = []
        self.num_info_obj_list = 0  # リストの数

        # オブジェクトを格納する辞書
        # キー値：ファイル名
        # 値：情報格納オブジェクト
        self.info_pri_obj_dict = {}
        self.num_info_obj_dict = 0  # 辞書の数

        self.file_error_tuplelist = []  # (エラーがあったファイル名 , 原因)

    # ------------------------------------------------------------
    # 情報入力1
    # ------------------------------------------------------------
    def input_csvfiles_pri(self):
        """
        自社側フォルダ内のcsvファイルの内容を取得

        入力：
            無し
        出力：
            flag_run:実行されれば1
        変更されるプロパティ値:
            info_pri_obj_dict:
                取得した情報のオブジェクトを格納する辞書配列
                (key値：拡張子付きファイル名、値：情報格納オブジェクト)
            file_error_tuplelist:
                (エラーがあったファイル名 , 原因)を格納するリスト
        """
        # パスの存在確認
        # flag_run:実行されれば1
        flag_run = os.path.exists(self.dir_path_pri)
        # print(flag_run)
        if flag_run:
            num_info_obj = 0  # 情報を格納したオブジェクトの数
            list_filenames = os.listdir(self.dir_path_pri)
            num_filenames = len(list_filenames)
            print("{}に格納されたファイルは{}個です".format(self.dir_path_pri, num_filenames))

            for filename in list_filenames:
                target_file_PATH1 = self.dir_path_pri + "/" + filename
                try:
                    # CSVファイルを開く
                    csv_file = open(target_file_PATH1, "r")

                    print("{}の情報を取得します...".format(filename))
                    # 拡張子の確認
                    root, ext = os.path.splitext(filename)
                    if ext == ".csv":
                        # 情報を格納するオブジェクトを作成
                        info_obj_unit = info_obj(filename, self.client_type)

                        readdatas = csv.reader(csv_file)

                        # CSVから1行ごとに情報取得
                        for readdata in readdatas:
                            info_obj_unit.input_info_list_pri(readdata)

                        # 辞書配列に格納
                        self.info_pri_obj_dict[filename] = info_obj_unit
                        num_info_obj = num_info_obj + 1
                    else:
                        print("{}はcsvファイルではありません。".format(filename))
                        self.file_error_tuplelist.append(
                            (target_file_PATH1, "csvファイルではありません")
                        )

                except Exception as e:
                    print("{}の情報取得に失敗しました".format(filename))
                    print(e, "error occurred")
                    print(traceback.format_exc())
                    self.file_error_tuplelist.append((target_file_PATH1, "情報取得に失敗しました"))

                # CSVファイルを閉じる
                csv_file.close()
            print("{}個のcsvファイルの情報を格納しました。".format(num_info_obj))
            self.num_info_obj_dict = num_info_obj
        else:
            print("{}はありません。".format(self.dir_path_pri))

        return flag_run

    # ------------------------------------------------------------
    # 情報入力2
    # ------------------------------------------------------------
    def input_csvfiles_client(self):
        """
        自社側フォルダ内のcsvファイルの内容を取得

        入力：
            無し
        出力：
            flag_run:実行されれば1
        変更されるプロパティ値:
            info_pri_obj_dict:
                比較を行うオブジェクトをpopで削除
            file_error_tuplelist:
                (エラーがあったファイル名 , 原因)を格納するリスト
            info_obj_list:
                情報格納オブジェクト「StructInfoForCSVCmp」のリスト
        """
        # パスの存在確認
        flag_run = os.path.exists(self.dir_path_client)
        if flag_run:
            num_info_obj = 0  # 情報を格納したオブジェクトの数
            list_filenames = os.listdir(self.dir_path_client)
            num_filenames = len(list_filenames)
            print("{}に格納されたファイルは{}個です".format(self.dir_path_client, num_filenames))

            for filename in list_filenames:
                target_file_PATH2 = self.dir_path_client + "/" + filename

                # 拡張子の確認
                root, ext = os.path.splitext(filename)
                if ext == ".csv":
                    # 情報を格納するオブジェクトを辞書からpopする。
                    try:
                        info_obj_unit = self.info_pri_obj_dict.pop(filename)
                    except Exception:
                        # popできなかった場合、dir_path_pri側に対応ファイルが存在していない
                        print("{}の情報がありませんでした".format(filename))
                        print(traceback.format_exc())
                        self.file_error_tuplelist.append(
                            (self.dir_path_pri + "/" + filename, "存在しません")
                        )
                        continue

                    try:
                        # CSVファイルを読み込み用で開く
                        csv_file = open(target_file_PATH2, "r")
                        print("{}の情報を取得します...".format(filename))
                        readdatas = csv.reader(csv_file)
                        # CSVから1行ごとに情報取得
                        for readdata in readdatas:
                            info_obj_unit.input_info_list_client(readdata)

                        # 比較を実行
                        info_obj_unit.cmp_info_list()

                        # オブジェクト配列に格納
                        self.info_obj_list.append(info_obj_unit)
                        num_info_obj = num_info_obj + 1
                    except Exception as e:
                        print("{}の情報取得に失敗しました".format(filename))
                        print(e, "error occurred")
                        print(traceback.format_exc())
                        self.file_error_tuplelist.append(
                            (target_file_PATH2, "情報が取得できません")
                        )

                    # CSVファイルを閉じる
                    csv_file.close()
                else:
                    print("{}はcsvファイルではありません。".format(filename))
                    self.file_error_tuplelist.append(
                        (target_file_PATH2, "csvファイルではありません")
                    )

            print("{}個のcsvファイルの情報を格納しました。".format(num_info_obj))
            self.num_info_obj_list = num_info_obj

            # 辞書の残りをエラーリストに追加
            for error_obj in self.info_pri_obj_dict.values():
                self.file_error_tuplelist.append(
                    (self.dir_path_client + "/" + error_obj.filename, "存在しません")
                )

        return flag_run
