# imports
import xlsxwriter
from datetime import datetime
import pandas as pd
from itertools import chain

import fun


class Storage:
    def __init__(self, methods_list, name="Project", hist_bins=10):
        self.name = name
        self.start_time = datetime.now()
        self.methods_list = methods_list
        self.hist_bins = hist_bins

        self.data_rounds = {}
        self.data_rounds_hist = {}
        self.data_rounds_ut = {}
        self.data_rounds_winners = {}

        self.statistics = {"Iterations": [],
                           "Candidates": [],
                           "Voters": [],
                           "PDF": [],
                           "PDF_type": [],
                           "Method": [],
                           "Condorcet": [],
                           "Condorcet loser": [],
                           "Max Utility": [],
                           "Min Utility": [],
                           "Majority_winner": [],
                           "Majority_loser": [],
                           "Condorcet_proportion": [],
                           "Condorcet_within_list": [],
                           "Multiple winners": [],
                           }

        self.statistics_full_hist = {"Candidates": [],
                                     "Voters": [],
                                     "PDF": [],
                                     "Method": []}
        self.statistics_full_ut = {"Candidates": [],
                                     "Voters": [],
                                     "PDF": [],
                                     "Method": []}

    def set_data_rounds(self):
        self.data_rounds = {}
        self.data_rounds_hist = {}
        self.data_rounds_ut = {}
        self.data_rounds_winners = {}

        self.data_rounds["Candidates"] = []
        self.data_rounds["Voters"] = []
        self.data_rounds["PDF"] = []

        for i in self.methods_list:
            self.data_rounds[i] = []
            self.data_rounds_hist[i] = []
            self.data_rounds_ut[i] = []
            self.data_rounds_winners[i] = []


    def create_process(self, process_no=1):
        self.data_rounds[process_no] = {}
        self.data_rounds_hist[process_no] = {}
        self.data_rounds_ut[process_no] = {}
        self.data_rounds_winners[process_no] = {}

        self.data_rounds[process_no]["Candidates"] = []
        self.data_rounds[process_no]["Voters"] = []
        self.data_rounds[process_no]["PDF"] = []

        for i in self.methods_list:
            self.data_rounds[process_no][i] = []
            self.data_rounds_hist[process_no][i] = []
            self.data_rounds_ut[process_no][i] = []
            self.data_rounds_winners[process_no][i] = []

    def one_round_process(self, data_in, data_in_hist, data_in_ut, data_in_winners, process_no=1, ):
        for i in data_in:
            self.data_rounds[process_no][i].append(data_in[i])

        for i in data_in_hist:
            self.data_rounds_hist[process_no][i].append(data_in_hist[i])

        for i in data_in_ut:
            self.data_rounds_ut[process_no][i].append(data_in_ut[i])

        for i in data_in_winners:
            self.data_rounds_winners[process_no][i].append(data_in_winners[i])

    def merge_processes(self):
        copy_dict = self.data_rounds.copy()
        copy_dict_hist = self.data_rounds_hist.copy()
        copy_dict_ut = self.data_rounds_ut.copy()
        copy_dict_winners = self.data_rounds_winners.copy()
        self.set_data_rounds()

        for i in copy_dict:
            for ii in copy_dict[i]:
                for iii in copy_dict[i][ii]:
                    self.data_rounds[ii].append(iii)

        for i in copy_dict_hist:
            for ii in copy_dict_hist[i]:
                for iii in copy_dict_hist[i][ii]:
                    self.data_rounds_hist[ii].append(iii)

        for i in copy_dict_ut:
            for ii in copy_dict_ut[i]:
                for iii in copy_dict_ut[i][ii]:
                    self.data_rounds_ut[ii].append(iii)

        for i in copy_dict_winners:
            for ii in copy_dict_winners[i]:
                for iii in copy_dict_winners[i][ii]:
                    self.data_rounds_winners[ii].append(iii)

    def aggregate_results(self, specific_pdf_type="na", max_candidates=11):
        for i in self.methods_list:
            self.statistics["Iterations"].append(len(self.data_rounds["Candidates"]))
            self.statistics["Candidates"].append(self.data_rounds["Candidates"][0])
            self.statistics["Voters"].append(self.data_rounds["Voters"][0])
            self.statistics["PDF"].append(self.data_rounds["PDF"][0])
            self.statistics["PDF_type"].append(specific_pdf_type)
            self.statistics["Method"].append(i)

            self.statistics["Condorcet"].append(fun.condorcet_compare(comparing=self.data_rounds[i],
                                                                      comparing_to=self.data_rounds["Condorcet"]))
            self.statistics["Condorcet loser"].append(fun.condorcet_compare(comparing=self.data_rounds[i],
                                                                            comparing_to=self.data_rounds["Condorcet_loser"]))

            self.statistics["Max Utility"].append(fun.compare(comparing=self.data_rounds[i],
                                                              comparing_to=self.data_rounds["Max Utility"]))

            self.statistics["Min Utility"].append(fun.compare(comparing=self.data_rounds[i],
                                                              comparing_to=self.data_rounds["Min Utility"]))

            self.statistics["Majority_winner"].append(fun.condorcet_compare(comparing=self.data_rounds[i],
                                                                            comparing_to=self.data_rounds["Majority_winner"]))

            self.statistics["Majority_loser"].append(fun.condorcet_compare(comparing=self.data_rounds[i],
                                                                           comparing_to=self.data_rounds["Majority_loser"]))

            self.statistics["Condorcet_proportion"].append(fun.condorcet_compare_proportion(comparing=self.data_rounds[i],
                                                                                            comparing_to=self.data_rounds["Condorcet"]))

            self.statistics["Condorcet_within_list"].append(fun.condorcet_compare_within_list(comparing=self.data_rounds[i],
                                                                                              comparing_to=self.data_rounds["Condorcet"]))

            self.statistics["Multiple winners"].append(fun.multiple_winners(input_list=self.data_rounds[i]))

            for ii in range(0, max_candidates + 1):
                self.statistics.setdefault("C{0}chosen".format(ii), []).append(fun.how_often_chosen(
                    input_list=self.data_rounds[i], unique_value=ii))

            # creates average of lists of all itterations
            histogram_list = fun.average_of_lists(input_lists=self.data_rounds_hist[i])

            # assign values to histogram bins
            for ii in range(len(histogram_list)):
                self.statistics.setdefault("Hist{0}".format(ii+1), []).append(histogram_list[ii])


            # save all histogram data
            self.statistics_full_hist["Candidates"].append(self.data_rounds["Candidates"][0])
            self.statistics_full_hist["Voters"].append(self.data_rounds["Voters"][0])
            self.statistics_full_hist["PDF"].append(self.data_rounds["PDF"][0])
            self.statistics_full_hist["Method"].append(i)

            for ii in range(self.hist_bins):
                appending_hist = []
                for iii in self.data_rounds_hist[i]:
                    appending_hist.append(iii[ii])
                self.statistics_full_hist.setdefault("Hist{0}".format(ii+1), []).append(appending_hist)

            # save all utility data
            self.statistics_full_ut["Candidates"].append(self.data_rounds["Candidates"][0])
            self.statistics_full_ut["Voters"].append(self.data_rounds["Voters"][0])
            self.statistics_full_ut["PDF"].append(self.data_rounds["PDF"][0])
            self.statistics_full_ut["Method"].append(i)
            self.statistics_full_ut.setdefault("Utility", []).append(list(chain.from_iterable(self.data_rounds_ut[i])))
            self.statistics_full_ut.setdefault("Winners", []).append(list(self.data_rounds_winners[i]))
            # chain.from_iterable(A)

        self.set_data_rounds()

    def export(self, start, end):
        writer = pd.ExcelWriter("{0}.xlsx".format(self.name), engine="xlsxwriter")
        df_all = pd.DataFrame.from_dict(self.statistics)
        df_all.to_excel(writer, sheet_name="AllData")
        info_log = pd.DataFrame({'Info:': 'This simulation was created using code available at: '
                                          'https://github.com/alotbsol/IH21_D21_comparison',
                                "Start time:": start,
                                "End time:": end,
                                 }, index=[0]).transpose()
        info_log.to_excel(writer, sheet_name="Info_log")

        writer.close()
