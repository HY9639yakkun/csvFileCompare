#!/usr/bin/env python
# coding: UTF-8

import tkinter
import tkinter.filedialog
import tkinter.ttk  # ドロップダウンリスト作成
import tkinter.messagebox  # GUI作成のツール
import os  # フォルダ操作関連
import datetime  # 時刻


##################################################
# UI作成クラス(基底)
##################################################
# Frame はwidgetをまとめるwidget。これを継承。
class BaseClassMakeInputUI(tkinter.Frame):
    """UI作成"""

    def __init__(self, master=None):
        super().__init__(master)  # 親クラス(tkinter.Frame)のコンストラクタ実行
        self.pack(expand=True, fill=tkinter.BOTH)
        self.master.title("入力してください")  # ウインドウ名
        self.configure(width=800, height=300, bg="lightgrey")
        self.master.resizable(1, 0)  # ウインドウサイズ変更有無。
        self.grid_columnconfigure(0, weight=1)  # gridで配置した1列目を伸縮するようにする

        # [X]実行時処理の上書き
        self.master.protocol("WM_DELETE_WINDOW", self.callback_Quit)

        self.get_dir_path_txt_list = []  # フォルダパスを入力するテキストボックスを格納するリスト
        self.RunFlag = False  # 実行されれば1
        self.path_list = []  # 取得したパスを格納

    ##################################################
    # widgetの配置
    ##################################################
    def func_create_widgets(self):
        """widgetの配置(上書き用)"""
        pass

    ##################################################
    # 関数
    ##################################################
    def callback_select_folfer(self, num):
        """ ファイル選択ダイアログの表示"""

        iDir = os.path.abspath(os.path.dirname(__file__))  # 現在のフォルダ

        # askdirectory ディレクトリを選択する。
        dirname = tkinter.filedialog.askdirectory(initialdir=iDir)

        # 処理ファイル名の出力
        self.get_dir_path_txt_list[num].delete(0, tkinter.END)  # テキストボックスをクリア
        self.get_dir_path_txt_list[num].insert(tkinter.END, dirname)

    ##################################################
    def callback_Quit(self):
        """終了(非実行)"""
        if tkinter.messagebox.askokcancel("Quit", "終了しますか?"):
            # self.master.destroy()#ウィンドウの削除
            self.destroy()
            self.quit()  # 終了

    ##################################################
    def func_check_input(self, mesTuple):
        """入力値チェック"""
        title_str = "入力値ERROR"
        fOutputNg = False  # 問題があれば1

        # 値が空でないことを確認
        # 存在するパスであることを確認
        for num in range(len(self.path_list)):  # num=0~1
            if len(self.path_list[num]) == 0:
                tkinter.messagebox.showwarning(
                    title_str, "{} が空です。".format(mesTuple[num])
                )
                fOutputNg = True
            elif not (os.path.exists(self.path_list[num])):
                tkinter.messagebox.showwarning(
                    title_str, "{} に入力されたPASSは存在しません。".format(mesTuple[num])
                )
                fOutputNg = True

        return fOutputNg

    ##################################################
    def callback_get_path(self):
        """完了確認時、UIに登録されたパスを取得"""
        pass

    ##################################################
    # 関数
    ##################################################


##################################################
# UI作成クラス(cscファイル格納フォルダパスの取得)
##################################################
class ClassMakeInputUIforCsv(BaseClassMakeInputUI):
    """UI作成"""

    def __init__(self, master=None):
        super().__init__(master)  # 親クラス(tkinter.Frame)のコンストラクタ実行
        self.master.title("csv格納フォルダのパスを入力してください")  # ウインドウ名

        self.stringTuple = ("自社", "客先")
        self.str_pattern = "sample"  # 選択されたパターン
        self.checkIDs = ("sample", "client1", "client2", "client3")

        ##################################################
        # UI作成
        ##################################################
        self.func_create_widgets()

    ##################################################
    def func_create_widgets(self):
        """widgetの配置"""
        pos_x = 40
        pos_y = 5
        common_hight = 12
        common_width = 80
        row_num = 0

        label_text = []
        Static = []

        button = []

        # コンボボックス####################
        row_num += 1
        cd_label = tkinter.Label(
            self, text="◎比較パターン", font=["", common_hight], bg="lightgrey"
        )
        cd_label.grid(row=row_num, column=0, padx=pos_x, pady=pos_y, sticky=tkinter.W)

        row_num += 1
        # Combobox の値は textvariable 属性で指定した変数にその都度格納される
        self.cb = tkinter.ttk.Combobox(self, state="readonly")

        # Combobox の選択が変更したときのコールバックは bind メソッドを用いて、
        # <<ComboboxSelected>> 仮想イベントにコールバック関数をアタッチ
        # self.cb.bind('<<ComboboxSelected>>', self.cb_selected)

        self.cb["values"] = self.checkIDs
        self.cb.current(0)  # デフォルト値
        self.cb.grid(
            row=row_num, column=0, padx=pos_x + 30, pady=pos_y, sticky=tkinter.W
        )

        row_num += 2

        for num in range(2):  # num=0~1
            # ラベル####################
            row_num += 1
            label_text.append("◎{}側のフォルダ".format(self.stringTuple[num]))
            # font=[,size,weight,slant,under,overstrike]
            Static.append(
                tkinter.Label(
                    self, text=label_text[num], font=["", common_hight], bg="lightgrey"
                )
            )
            Static[num].grid(
                row=row_num, column=0, padx=pos_x, pady=pos_y, sticky=tkinter.W
            )

            # テキストボックス(Entry)####################
            row_num += 1
            self.get_dir_path_txt_list.append(
                tkinter.Entry(
                    self,
                    font=["", common_hight],
                    width=common_width,
                    relief=tkinter.GROOVE,
                    bd=2,
                )
            )
            self.get_dir_path_txt_list[num].grid(
                row=row_num,
                column=0,
                padx=pos_x,
                pady=pos_y,
                sticky=tkinter.W + tkinter.E,
            )
            self.get_dir_path_txt_list[num].insert(tkinter.END, "")  # 初期値

            # ボタン####################
            # 引数有りのためラムダ式で関数を登録
            row_num += 1
            if num == 0:
                def command_func(): self.callback_select_folfer(0)
            else:
                def command_func(): self.callback_select_folfer(1)
            button.append(tkinter.Button(self, text="フォルダ選択", command=command_func))
            button[num].grid(
                row=row_num, column=0, padx=pos_x + 30, pady=pos_y, sticky=tkinter.W
            )

        # 完了ボタン####################
        row_num += 2
        button_comf = tkinter.Button(self, text="完了", command=self.callback_get_path)
        button_comf.grid(
            row=row_num, column=0, padx=pos_x, pady=pos_y, sticky=tkinter.E
        )

    ##################################################
    # 関数
    ##################################################
    def callback_get_path(self):
        """完了確認時、UIに登録されたパスを取得"""

        self.path_list.clear()  # リスト内の値を一度削除
        self.path_list.append(self.get_dir_path_txt_list[0].get())
        self.path_list.append(self.get_dir_path_txt_list[1].get())

        self.str_pattern = self.cb.get()

        # 入力値確認
        errorFlag = self.func_check_input(self.stringTuple)
        if errorFlag:
            return

        errorFlag = self.func_check_input_unique()
        if errorFlag:
            return

        messageStr = "比較パターン:" + self.str_pattern + "\n\n"

        messageStr1 = "取得したパスはこれでよろしいでしょうか？\n\n"
        # メッセージ作成
        for str_unit, str_path in zip(self.stringTuple, self.path_list):
            messageStr1 = messageStr1 + str_unit + "\n " + str_path + "\n"

        messageStr2 = messageStr + messageStr1
        ansFlag = tkinter.messagebox.askyesno("取得PATHの確認", messageStr2)

        if ansFlag:
            self.RunFlag = True
            self.destroy()
            self.quit()  # 終了

    ##################################################
    def func_check_input_unique(self):
        if self.path_list[0] == self.path_list[1]:
            tkinter.messagebox.showwarning("入力値ERROR", "同じPASSを比較しています。")
            fOutputNg = True
        else:
            fOutputNg = False

        return fOutputNg


##################################################
# UI作成クラス(日付の取得)
##################################################
class ClassMakeInputUIforDate(BaseClassMakeInputUI):
    """日付の取得UI"""

    def __init__(self, master=None):
        super().__init__(master)  # 親クラス(tkinter.Frame)のコンストラクタ実行
        self.master.title("確認する'月'を入力してください")  # ウインドウ名

        obj_today = datetime.date.today()
        self.target_year = obj_today.year
        self.target_month = obj_today.month

        ##################################################
        # UI作成
        ##################################################
        self.func_create_widgets()

    ##################################################
    def func_create_widgets(self):
        """widgetの配置"""
        pos_x = 40
        pos_y = 5
        common_hight = 12
        # common_width = 80
        row_num = 0

        # コンボボックス(年)####################
        row_num += 1
        cd_label_year = tkinter.Label(
            self, text="◎年", font=["", common_hight], bg="lightgrey"
        )
        cd_label_year.grid(
            row=row_num, column=0, padx=pos_x, pady=pos_y, sticky=tkinter.W
        )
        row_num += 1
        # Combobox の値は textvariable 属性で指定した変数にその都度格納される
        self.cb_year = tkinter.ttk.Combobox(self, state="readonly")
        self.cb_year["values"] = [
            str(x)
            for x in (self.target_year - 2, self.target_year - 1, self.target_year)
        ]
        self.cb_year.current(2)  # デフォルト値
        self.cb_year.grid(
            row=row_num, column=0, padx=pos_x + 30, pady=pos_y, sticky=tkinter.W
        )

        # コンボボックス(月)####################
        row_num += 1
        cd_label_month = tkinter.Label(
            self, text="◎月", font=["", common_hight], bg="lightgrey"
        )
        cd_label_month.grid(
            row=row_num, column=0, padx=pos_x, pady=pos_y, sticky=tkinter.W
        )
        row_num += 1
        # Combobox の値は textvariable 属性で指定した変数にその都度格納される
        self.cb_month = tkinter.ttk.Combobox(self, state="readonly")
        self.cb_month["values"] = [
            str(x) for x in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        ]
        self.cb_month.current(self.target_month - 1)  # デフォルト値
        self.cb_month.grid(
            row=row_num, column=0, padx=pos_x + 30, pady=pos_y, sticky=tkinter.W
        )

        # 完了ボタン####################
        row_num += 2
        button_comf = tkinter.Button(self, text="完了", command=self.func_get_date)
        button_comf.grid(
            row=row_num, column=0, padx=pos_x, pady=pos_y, sticky=tkinter.E
        )

    ##################################################
    # コールバック関数
    ##################################################
    def func_get_date(self):
        self.target_year = int(self.cb_year.get())
        self.target_month = int(self.cb_month.get())

        messageStr = (
            str(self.target_year) + "年" + str(self.target_month) + "月について確認を行います"
        )
        ansFlag = tkinter.messagebox.askyesno("対象月確認", messageStr)

        if ansFlag:
            self.RunFlag = True
            self.destroy()
            self.quit()


##################################################
# UI作成クラス(結果格納フォルダの取得)
##################################################
class ClassMakeInputUIforResultDir(BaseClassMakeInputUI):
    """結果格納フォルダの取得UI"""

    def __init__(self, master=None):
        super().__init__(master)  # 親クラス(tkinter.Frame)のコンストラクタ実行
        self.master.title("結果レポートの出力先を入力してください")  # ウインドウ名

        ##################################################
        # UI作成
        ##################################################
        self.func_create_widgets()

    ##################################################
    def func_create_widgets(self):
        """widgetの配置"""
        pos_x = 40
        pos_y = 5
        common_hight = 12
        common_width = 80
        row_num = 0

        Static = []
        button = []

        num = 0
        # ラベル####################
        row_num += 1
        # font=[,size,weight,slant,under,overstrike]
        Static.append(
            tkinter.Label(
                self, text="◎結果格納フォルダ", font=["", common_hight], bg="lightgrey"
            )
        )
        Static[num].grid(
            row=row_num, column=0, padx=pos_x, pady=pos_y, sticky=tkinter.W
        )

        # テキストボックス(Entry)####################
        row_num += 1
        self.get_dir_path_txt_list.append(
            tkinter.Entry(
                self,
                font=["", common_hight],
                width=common_width,
                relief=tkinter.GROOVE,
                bd=2,
            )
        )
        self.get_dir_path_txt_list[num].grid(
            row=row_num, column=0, padx=pos_x, pady=pos_y, sticky=tkinter.W + tkinter.E
        )
        self.get_dir_path_txt_list[num].insert(tkinter.END, "")  # 初期値

        # ボタン####################
        row_num += 1
        def command_func(): self.callback_select_folfer(0)  # 引数有りのためラムダ式で関数を登録
        button.append(tkinter.Button(self, text="フォルダ選択", command=command_func))
        button[num].grid(
            row=row_num, column=0, padx=pos_x + 30, pady=pos_y, sticky=tkinter.W
        )

        # 完了ボタン####################
        row_num += 2
        button_comf = tkinter.Button(self, text="完了", command=self.callback_get_path)
        button_comf.grid(
            row=row_num, column=0, padx=pos_x, pady=pos_y, sticky=tkinter.E
        )

    ##################################################
    # 関数
    ##################################################
    def callback_get_path(self):
        """完了確認時、UIに登録されたパスを取得"""

        self.path_list.clear()  # リスト内の値を一度削除
        self.path_list.append(self.get_dir_path_txt_list[0].get())

        # 入力値確認
        errorFlag = self.func_check_input(("結果格納フォルダ"))
        if errorFlag:
            return

        messageStr1 = "取得したパスはこれでよろしいでしょうか？\n\n"
        # メッセージ作成
        messageStr1 = messageStr1 + self.path_list[0] + "\n"
        ansFlag = tkinter.messagebox.askyesno("取得PATHの確認", messageStr1)

        if ansFlag:
            self.RunFlag = True
            self.destroy()
            self.quit()  # 終了


##################################################
# 実行関数
##################################################
def funcGetCsvFilesDirPathUI():
    """
    チェック対象csvファイルのフォルダパス取得UI
    """
    obj1 = ClassMakeInputUIforCsv()
    obj1.pack()
    obj1.mainloop()  # ループ終端

    result0 = obj1.RunFlag  # 実行されれば1
    result1 = obj1.path_list  # 比較対象フォルダ
    result2 = obj1.str_pattern  # 比較パターン
    return result0, result1, result2


def funcGetDateUI():
    """
    日付の取得UI
    """
    obj1 = ClassMakeInputUIforDate()
    obj1.pack()
    obj1.mainloop()  # ループ終端

    result0 = obj1.RunFlag
    result1 = obj1.target_year
    result2 = obj1.target_month
    return result0, result1, result2


def funcGetResultDirUI():
    """結果格納フォルダの取得UI"""
    obj1 = ClassMakeInputUIforResultDir()
    obj1.pack()
    obj1.mainloop()  # ループ終端

    result0 = obj1.RunFlag
    if result0:
        result1 = obj1.path_list[0]
    else:
        print("結果の格納先を取得しませんでした\n")
        result1 = []
    return result0, result1
