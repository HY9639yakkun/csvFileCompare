#!/usr/bin/env python
# coding: UTF-8

import calendar  # カレンダー1
import datetime  # 時刻
import traceback  # エラー情報
import webbrowser  # ファイルを開く

from funcMakeInputUI import funcGetCsvFilesDirPathUI  # 入力UI作成関数
from funcMakeInputUI import funcGetDateUI
from funcMakeInputUI import funcGetResultDirUI
from ClassGetCSVInfo import ClassGetCSVInfo as get_csv_class  # 情報取得オブジェクト


def RunCSVCmp():
    """
    比較を行う関数
    出力:
        flag_run:
            比較が行われれば1
        get_csv_obj:
            比較結果などを格納したオブジェクト「ClassGetCSVInfo」
    """

    runFlag_GetDate, thisYear, thisMomth = funcGetDateUI()
    if runFlag_GetDate:
        runFlag1, pathAry, pattern = funcGetCsvFilesDirPathUI()  # UIを実行、情報取得
        if runFlag1:
            print("runFlag：{}\n".format(runFlag1))
            print("pattern：{}\n".format(pattern))
            print("path1：{}\n".format(pathAry[0]))
            print("path2：{}\n".format(pathAry[1]))
            print("Year：{}\n".format(thisYear))
            print("Momth：{}\n".format(thisMomth))
    else:
        runFlag1 = False

    if runFlag1:
        # オブジェクトの作成
        get_csv_obj = get_csv_class(pathAry[0], pathAry[1], pattern)

        # 自社側のcsvファイルを入力
        runFlag2_1 = get_csv_obj.input_csvfiles_pri()

        print("--------------------------------------------------\n")
        if runFlag2_1:
            # 客先側のcsvファイルを入力
            runFlag2_2 = get_csv_obj.input_csvfiles_client()
        else:
            runFlag2_2 = False
        print("--------------------------------------------------\n")

        flag_run = runFlag2_1 and runFlag2_2
        if not (flag_run):
            print("比較は行われませんでした\n")
    else:
        print("実行しませんでした\n")
        flag_run = False
        get_csv_obj = []
        thisYear = []
        thisMomth = []

    return flag_run, get_csv_obj, thisYear, thisMomth


def writeResultToHtml(outputFile, info_obj, date_num_all):
    """
    結果の書き込み
    結果がNGの場合はファイル名を返す
    """
    ngFileName = ""

    indresult2HtmlIdTuple = (
        "ind_result_NG",
        "ind_result_OK",
        "ind_result_Nothing",
    )  # 個別結果用Html ID
    dispMessTuple = ("NG", "OK", "-", "PASS")  # 表示するメッセージ
    result2HtmlIdTuple = (
        "result_NG",
        "result_OK",
        "result_NOTHING",
        "result_PASS",
    )  # 総合結果用Html ID

    outputFile.write("<tr>\n")
    outputFile.write("<th>{}</th>".format(info_obj.filename))
    outputFile.write("\n")

    info_num_all = len(info_obj.cmp_result_ind_list)  # 日付ごとの結果の数
    for date_num in range(1, date_num_all + 1):
        # 日付ごとの結果書き込み
        if date_num <= info_num_all:
            info_index = date_num - 1
            result_ind = info_obj.cmp_result_ind_list[info_index]  # 0:NG 1:OK
            outputFile.write(
                '<td class="{}"><p>{}</p></td>\n'.format(
                    indresult2HtmlIdTuple[result_ind], dispMessTuple[result_ind]
                )
            )
        else:
            # 結果が日数に対して不足
            outputFile.write(
                '<td class="{}"><p>{}</p></td>\n'.format(
                    indresult2HtmlIdTuple[2], dispMessTuple[2]
                )
            )
    # 個人ごとの総合結果書き込み
    if info_obj.cmp_result_flag and (date_num == info_num_all):
        cmp_result_num_for_report = 3  # PASS(完全にOK)
    else:
        cmp_result_num_for_report = info_obj.cmp_result_flag

        if cmp_result_num_for_report == 0:
            ngFileName = info_obj.filename

    outputFile.write(
        '<td class="{}"><p>{}</p></td>\n'.format(
            result2HtmlIdTuple[cmp_result_num_for_report],
            dispMessTuple[cmp_result_num_for_report],
        )
    )
    outputFile.write("</tr>\n")

    return cmp_result_num_for_report, ngFileName


def makeGenForCSS():
    """
    CSS文作成用ジェネレータ作成
    """

    yield '<style type="text/css">\n'
    yield ".ind_result_NG { color: red; }\n"
    yield ".result_OK { font-weight:bold; }\n"
    yield ".result_NG { color: red; font-weight:bold; }\n"
    yield ".result_PASS { color: green; font-weight:bold; }\n"
    yield ".ind_result_Nothing {background-color: #ddd;}\n"
    yield "table { border-collapse: collapse; }\n"
    yield "th{ width: 12%; padding: 6px; text-align: right;\n"
    yield "vertical-align: top; color: #333; background-color: #eee;\n"
    yield "border: 1px solid #b9b9b9; }\n"
    yield "td{ padding: 6px; background-color: #fff;\n"
    yield "border: 1px solid #b9b9b9; text-align: center; }\n"
    yield "</style>\n"


##################################################
# 実行
##################################################
def run_csv_cmp():
    flag_run, get_csv_obj, thisYear, thisMomth = RunCSVCmp()

    if flag_run:
        runFlag_ResultDir, result_dir_path = funcGetResultDirUI()
        if not (runFlag_ResultDir):
            print("実行を中止しました\n")
            outputFilePath = None
            return outputFilePath

        todaydetail = datetime.datetime.today()
        nowTimeStr = todaydetail.strftime("%Y%m%d%H%M")
        outputFilePath0 = r"\result_test_"
        outputFilePath = result_dir_path + outputFilePath0 + nowTimeStr + ".html"
        print("出力ファイル : {}\n".format(outputFilePath))

        ngFileNameList = []
        dayNum2YoubiTuple = ("SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT")
        encoStr = "utf-8"
        c1 = calendar.Calendar()
        try:
            outputFile = open(outputFilePath, "w", encoding=encoStr)  # 書き込みモードで開く

            # ヘッダ作成###############################################
            outputFile.write("<!DOCTYPE html>\n")
            outputFile.write('<html lang="ja">\n')
            outputFile.write("<head>\n")
            outputFile.write('<meta charset="' + encoStr + '"/>\n')
            outputFile.write("<title>compare result</title>\n")
            outputFile.write("</head>\n")
            #######################################################

            # CSS作成###############################################
            cssStringGen = makeGenForCSS()
            for cssString in cssStringGen:
                outputFile.write(cssString)
            #######################################################

            outputFile.write("<body>\n")
            # 情報##################################################
            outputFile.write("<p><font>日付 : {}</p>\n".format(nowTimeStr))
            outputFile.write(
                "<p><font>比較パターン : {}</font></p>\n".format(get_csv_obj.client_type)
            )
            outputFile.write(
                "<p><font>PATH1 : {}</font></p>\n".format(get_csv_obj.dir_path_pri)
            )
            outputFile.write(
                "<p><font>PATH2 : {}</font></p>\n".format(get_csv_obj.dir_path_client)
            )
            outputFile.write("<br>\n")
            #######################################################

            # 日付別結果##################################################
            info_obj_len = len(get_csv_obj.info_obj_list)
            outputFile.write("<h3>日付別比較結果({})</h3>\n".format(info_obj_len))
            # 日付##################################################
            date_num_all = 0  # 日数
            outputFile.write("<table>\n")
            outputFile.write("<tr>\n")
            outputFile.write("<th>date</th>\n")
            for date_str, ele in zip(
                c1.itermonthdates(thisYear, thisMomth),
                c1.itermonthdays2(thisYear, thisMomth),
            ):
                if not (ele[0] == 0):
                    date_num_all = date_num_all + 1
                    youbiStr = dayNum2YoubiTuple[ele[1]]  # 曜日
                    outputFile.write(
                        '<td class="date"><p>{}({})</p></td>\n'.format(
                            date_str, youbiStr
                        )
                    )

            outputFile.write('<td class="result"><p>RESULT</p></td>\n')
            outputFile.write("</tr>\n")
            #######################################################
            all_path_flag = True
            for info_obj in get_csv_obj.info_obj_list:
                # 結果の書き込み##################################################
                cmp_result_num_for_report, ngFileName = writeResultToHtml(
                    outputFile, info_obj, date_num_all
                )
                if all_path_flag:
                    if not (cmp_result_num_for_report == 3):
                        all_path_flag = False
                if not (ngFileName == ""):
                    ngFileNameList.append(ngFileName)
                #######################################################
            outputFile.write("</table>\n")
            if all_path_flag:
                outputFile.write('<p><font color="green">全てPASSしました</font></p>\n')
                outputFile.write("<br>\n")

            # NGリスト##################################################
            ngFileLen = len(ngFileNameList)
            if ngFileLen == 0:
                outputFile.write("<h3>比較結果NGはありませんでした</h3>\n")
            else:
                outputFile.write(
                    "<h3>比較結果NGファイルリスト({}/{})</h3>\n".format(ngFileLen, info_obj_len)
                )
                outputFile.write("<ul>\n")
                for ngFileName in ngFileNameList:
                    outputFile.write("<li>{}</li>\n".format(ngFileName))
                outputFile.write("</ul>\n")

            outputFile.write("<br>\n")

            # チェック不可ファイルリスト##################################################
            file_error_len = len(get_csv_obj.file_error_tuplelist)
            if not (file_error_len == 0):
                outputFile.write(
                    "<h3>比較チェック不可ファイルリスト({})</h3>\n".format(file_error_len)
                )
                outputFile.write('<table id="NotCheck">\n')
                outputFile.write("<tr>\n")
                outputFile.write("<td><p>ファイルパス</p></td>\n")
                outputFile.write("<td><p>原因</p></td>\n")
                outputFile.write("</tr>\n")
                for file_error_tuple in get_csv_obj.file_error_tuplelist:
                    outputFile.write("<tr>\n")
                    outputFile.write("<td><p>{}</p></td>\n".format(file_error_tuple[0]))
                    outputFile.write("<td><p>{}</p></td>\n".format(file_error_tuple[1]))
                    outputFile.write("</tr>\n")
                outputFile.write("</table>\n")

            outputFile.write("</body>\n")
            outputFile.write("</html>\n")
        except Exception as e:
            print("結果書き込み中にエラーが発生しました。")
            print(e, "error occurred")
            print(traceback.format_exc())
            outputFilePath = None
        finally:
            outputFile.close()
    else:
        outputFilePath = None

    return outputFilePath


if __name__ == "__main__":
    outputFilePath = run_csv_cmp()
    if not (outputFilePath is None):
        try:
            webbrowser.open(outputFilePath)
        except Exception as e:
            print("レポートが開けませんでした")
            print(e, "error occurred")
            print(traceback.format_exc())
    print("終了\n")
