#!/usr/bin/env python3

"""
Do a local practice grading.
The score you recieve here is not an actual score,
but gives you an idea on how prepared you are to submit to the autograder.
"""
import types
import os
import sys
import chess

import autograder.assignment
import autograder.cmd.gradeassignment
import autograder.question
import autograder.style
import utils

import inspect

class Assignment2(autograder.assignment.Assignment):
    def __init__(self, **kwargs):
        super().__init__(questions = [
            Q1(20, "Question 1", timeout=90),
            Q2(15, "Question 2", timeout=120),
            Q3(5, "Question 3", timeout=60),
            Q4(10, "Question 4", timeout=30),
            Q5(10, "Question 5", timeout=30)
            ], **kwargs)

class Q1(autograder.question.Question):
    def score_question(self, submission):
        try:
            minimax = submission.__all__.get_minimax_move
            if (self.check_not_implemented(minimax)):
                self.add_message("Not Implemented Error")
                return

            cases = [
            ("Board 0 Trivial", chess.Board("rn3r2/5p1k/2p2p1p/1pqppP1Q/6N1/3PP2P/2P3P1/1q2R1K1"), 1, "e1b1", 10),
            ("Board 1 Medium", chess.Board("pppp4/5k1r/pppp3p/8/pppp4/5n1R/8/2K5"), 3, "h3f3", 5),
            ("Board 2 Medium", chess.Board("kp4pp/p3B3/3p1b2/2q3b1/2ppppp1/p6p/K7/8"), 3, "e7f6", 5)
            ]
            
            for i in range(0, len(cases)):
                case_name, case_board, case_depth, case_ans, case_pts = cases[i]
                
                student_ans = utils.testAdvSearch(minimax, utils.evaluation, case_board, case_depth)

                msg = (f"{case_name} ({case_pts} pts): {student_ans} ")
                if str(student_ans) == case_ans:
                    msg += "passed"
                    self.add_score(case_pts)
                else:
                    msg += "not passed"
                self.add_message(msg)
        except:
            self.add_message("Exception thrown during testing")

class Q2(autograder.question.Question):
    def score_question(self, submission):
        try:
            expectimax = submission.__all__.get_expectimax_move
            if (self.check_not_implemented(expectimax)):
                self.add_message("Not Implemented Error")
                return

            cases = [
            ("Board 1 Trivial", chess.Board("pppp4/5k1r/pppp3p/8/pppp4/5n1R/8/2K5"), 2, "h3h6", 5),
            ("Board 2 Medium", chess.Board("kp4pp/p3B3/3p1b2/2q3b1/2ppppp1/p6p/K7/8"), 2, "e7d6", 10),
            ]
            
            for i in range(0, len(cases)):
                case_name, case_board, case_depth, case_ans, case_pts = cases[i]
                
                student_ans = utils.testAdvSearch(expectimax, utils.evaluation, case_board, case_depth)

                msg = (f"{case_name} ({case_pts} pts): {student_ans} ")
                if str(student_ans) == case_ans:
                    msg += "passed"
                    self.add_score(case_pts)
                else:
                    msg += "not passed"
                self.add_message(msg)

        except:
            self.add_message("Exception thrown during testing")

class Q3(autograder.question.Question):
    def score_question(self, submission):
        # return
        # intended to encourage a new 'checkmate' element to the position scoring function.
        try:
            minimax = submission.__all__.get_minimax_move
            if (self.check_not_implemented(minimax)):
                self.add_message("Not Implemented Error for 'get_minimax_move")
                return
            
            pos_score = submission.__all__.get_position_score
            if (self.check_not_implemented(pos_score)):
                self.add_message("Not Implemented Error for 'get_position_score'")
                return

            cases = [
            ("Puzzle 1 Visible", chess.Board("1rr5/p1p2Rpp/2Qpk3/4n1q1/4P3/8/PPP3PP/R6K"), 1, "c6d5", 5)
            ]
            
            for i in range(0, len(cases)):
                case_name, case_board, case_depth, case_ans, case_pts = cases[i]
                
                student_ans = utils.testAdvSearch(minimax, pos_score, case_board, case_depth)

                msg = (f"{case_name} ({case_pts} pts): your move was {student_ans} ")
                if str(student_ans) == case_ans:
                    msg += "(passed)"
                    self.add_score(case_pts)
                else:
                    msg += "(not passed)"
                self.add_message(msg)
                
        except:
            self.add_message("Exception thrown during testing")

class Q4(autograder.question.Question):
    def score_question(self, submission):
        try:
            minimax = submission.__all__.get_minimax_move
            if (self.check_not_implemented(minimax)):
                self.add_message("Not Implemented Error for 'get_minimax_move")
                return
            
            pos_score = submission.__all__.get_position_score
            if (self.check_not_implemented(pos_score)):
                self.add_message("Not Implemented Error for 'get_position_score'")
                return

            cases = [
            ("Puzzle 2 Visible", chess.Board("8/1r3k2/2r1ppp1/8/5PB1/4P3/4PK2/5R2"), 3, "g4f3", 10)
            ]
            
            for i in range(0, len(cases)):
                case_name, case_board, case_depth, case_ans, case_pts = cases[i]
                
                student_ans = utils.testAdvSearch(minimax, pos_score, case_board, case_depth)

                msg = (f"{case_name} ({case_pts} pts):  your move was {student_ans} ")
                if str(student_ans) == case_ans:
                    msg += "(passed)"
                    self.add_score(case_pts)
                else:
                    msg += "(not passed)"
                self.add_message(msg)
                
        except:
            self.add_message("Exception thrown during testing")

class Q5(autograder.question.Question):
    def score_question(self, submission):
        try:
            minimax = submission.__all__.get_minimax_move
            if (self.check_not_implemented(minimax)):
                self.add_message("Not Implemented Error for 'get_minimax_move")
                return
            
            pos_score = submission.__all__.get_position_score
            if (self.check_not_implemented(pos_score)):
                self.add_message("Not Implemented Error for 'get_position_score'")
                return

            cases = [
            ("Puzzle 3 Visible", chess.Board("1k6/2b2p2/2p1p3/1pP2p2/1P1P1P2/8/2N1P3/1K6"), 1, "e2e3", 10)
            ]
            
            for i in range(0, len(cases)):
                case_name, case_board, case_depth, case_ans, case_pts = cases[i]
                
                student_ans = utils.testAdvSearch(minimax, pos_score, case_board, case_depth)

                msg = (f"{case_name} ({case_pts} pts):  your move was {student_ans} ")
                if str(student_ans) == case_ans:
                    msg += "(passed)"
                    self.add_score(case_pts)
                else:
                    msg += "(not passed)"
                self.add_message(msg)
                
        except:
            self.add_message("Exception thrown during testing")

def main(path):
    assignment = Assignment2(input_dir = path)
    result = assignment.grade()

    print("***")
    print("This is NOT an actual grade, submit to the autograder for an actual grade.")
    print("***\n")

    print(result.report())

def _load_args(args):
    exe = args.pop(0)
    if (len(args) != 1 or ({'h', 'help'} & {arg.lower().strip().replace('-', '') for arg in args})):
        print("USAGE: python3 %s <submission path (.py or .ipynb)>" % (exe), file = sys.stderr)
        sys.exit(1)

    path = os.path.abspath(args.pop(0))

    return path

if (__name__ == '__main__'):
    main(_load_args(list(sys.argv)))
