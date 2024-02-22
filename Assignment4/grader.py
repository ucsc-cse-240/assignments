#!/usr/bin/env python3

import types
import sys

import autograder.assignment
import autograder.cmd.gradeassignment
import autograder.question
import autograder.style
import utils
import data
import production # forward chain
import numpy

class Assignment4(autograder.assignment.Assignment):
    def __init__(self, **kwargs):
        super().__init__(questions = [
            Q1(10, "Question 1"),
            Q2(25, "Question 2"),
            Q3(15, "Question 3"),
            Q4(15, "Question 4"),
            Q5(10, "Question 5"),
            Q6(25, "Question 6")],**kwargs)
        #     autograder.style.Style(kwargs.get('input_dir'), max_points = 0),
        # ], **kwargs)

class Q1(autograder.question.Question):
    def score_question(self, submission):
        part1 = submission.__all__.p1_part1
        answer1 = part1()

        if (self.check_not_implemented(answer1)):
            return
        
        if answer1 < .08 and answer1 > .07:
            self.add_score(5)
        else:
            self.add_message("Incorrect solution to part 1")

        part2 = submission.__all__.p1_part2
        answer2 = part2()
        if answer2 < .24 and answer2 > .23:
            self.add_score(5)
        else:
            self.add_message("Incorrect solution to part 2")
        
class Q2(autograder.question.Question):
    def score_question(self, submission):
        part1 = submission.__all__.p2_part1
        answer1 = part1()
        
        if answer1 <= .027 and answer1> .02:
            self.add_score(5)
        elif answer1 >= 1:
            self.add_message("Incorrect solution to Q2 part 1.  Make sure answer is between 0 and 1.")
        else:
            self.add_message("Incorrect solution to Q2 part 1.")

        part2 = submission.__all__.p2_part2
        answer2 = part2()
        
        if answer2 <= 0.2 and answer2 > .15: # Answer is 0.178
            self.add_score(5)
        elif answer2 >= 1:
            self.add_message("Incorrect solution to Q2 part 2.  Make sure answer is between 0 and 1.")
        else:
            self.add_message("Incorrect solution to Q2 part 2.")

        part3 = submission.__all__.p2_part3
        answer3 = part3()
        
        if answer3 >= 0.2 and answer3 < .28: # Answer is .2225
            self.add_score(5)
        elif answer3 >= 1:
            self.add_message("Incorrect solution to Q2 part 3.  Make sure answer is between 0 and 1.")
        else:
            self.add_message("Incorrect solution to Q2 part 3.")

        part4 = submission.__all__.p2_part4
        ind,no_ind = part4()

        if int(ind) == 10:
            self.add_score(5)
        else:
            self.add_message("Incorrect answer to part 3 with mutual independent")

        if int(no_ind) <= 64 and int(no_ind) > 60:
            self.add_score(5)
        else:
            self.add_message("Incorrect answer to part 4 with no independence.")

        
class Q3(autograder.question.Question):
    def score_question(self, submission):
        part1 = submission.__all__.p3_part1
        part2 = submission.__all__.p3_part2
        part3 = submission.__all__.p3_part3

        if part1() == '2' or str(part1()) == '2':
            self.add_score(5)
        else:
            self.add_message("Incorrect solution for part1")

        if part2() == '0' or str(part2()) == '0':
            self.add_score(5)
        else:
            self.add_message("Incorrect solution for part2. Remember the special note about NOT.")

        if part3() == '3' or str(part3()) == '3':
            self.add_score(5)
        else:
            self.add_message("Incorrect solution for part3.  Remember the special note about NOT.")
        
class Q4(autograder.question.Question):
    def score_question(self, submission):
        transitive_rule = submission.__all__.transitive_rule

        abc_answer = production.forward_chain([transitive_rule()], data.abc_data)
        abc_solution = ('a beats b', 'b beats c', 'a beats c')
        if set(abc_answer) == set(abc_solution):
            self.add_score(5)
        else:
            self.add_message("Incorrect solution for abc_data")

        poker_answer = production.forward_chain([transitive_rule()], data.poker_data)
        poker_solution = ('two-pair beats pair', 'three-of-a-kind beats two-pair', 'straight beats three-of-a-kind',
                          'flush beats straight', 'full-house beats flush', 'straight-flush beats full-house',
                          'three-of-a-kind beats pair', 'straight beats two-pair', 'straight beats pair',
                          'flush beats three-of-a-kind', 'flush beats two-pair', 'flush beats pair', 'full-house beats straight',
                          'full-house beats three-of-a-kind', 'full-house beats two-pair', 'full-house beats pair',
                          'straight-flush beats flush', 'straight-flush beats straight', 'straight-flush beats three-of-a-kind',
                          'straight-flush beats two-pair', 'straight-flush beats pair')
        if set(poker_answer) == set(poker_solution):
            self.add_score(5)
        else:
            self.add_message("Incorrect solution for poker data.")
            
        minecraft_answer = production.forward_chain([transitive_rule()], data.minecraft_data)
        minecraft_solution = ('diamond-sword beats diamond-axe',
                              'stone-pick beats stone-shovel', 'diamond-axe beats iron-axe',
                              'iron-axe beats stone-shovel', 'iron-pick beats stone-pick',
                              'iron-axe beats iron-pick', 'stone-shovel beats fist',
                              'diamond-sword beats iron-axe', 'stone-pick beats fist',
                              'diamond-axe beats stone-shovel', 'diamond-sword beats stone-shovel',
                              'diamond-axe beats iron-pick', 'diamond-sword beats iron-pick',
                              'iron-axe beats fist', 'diamond-axe beats fist',
                              'diamond-sword beats fist', 'iron-pick beats stone-shovel',
                              'iron-pick beats fist', 'iron-axe beats stone-pick',
                              'diamond-axe beats stone-pick', 'diamond-sword beats stone-pick')
        if set(minecraft_answer) == set(minecraft_solution):
            self.add_score(5)
        else:
            self.add_message("Incorrect solution for minecraft data.")
        

class Q5(autograder.question.Question):
    def score_question(self, submission):
        family_rules = submission.__all__.family_rules

        simpson_solution = ('person bart', 'person lisa', 'person maggie', 'person marge', 'person homer', 'person abe',
                          'parent marge bart', 'parent marge lisa', 'parent marge maggie', 'parent homer bart',
                          'parent homer lisa', 'parent homer maggie', 'parent abe homer', 'self bart bart', 'self lisa lisa',
                          'self maggie maggie', 'self marge marge', 'self homer homer', 'self abe abe', 'sibling bart lisa',
                          'sibling bart maggie', 'sibling lisa bart', 'sibling lisa maggie', 'sibling maggie bart',
                          'sibling maggie lisa', 'child bart marge', 'child lisa marge', 'child maggie marge', 'child bart homer',
                          'child lisa homer', 'child maggie homer', 'child homer abe', 'grandparent abe bart', 'grandparent abe lisa',
                          'grandparent abe maggie', 'grandchild bart abe', 'grandchild lisa abe', 'grandchild maggie abe')
        simpson_answer = production.forward_chain(family_rules(), data.simpsons_data, verbose=False)
        if set(simpson_solution) == set(simpson_answer):
            self.add_score(5)
        else:
            self.add_message("Incorrect solution for simpsons data")

        black_family_cousins_solution = ['cousin sirius bellatrix', 'cousin sirius andromeda', 'cousin sirius narcissa',
                                'cousin regulus bellatrix', 'cousin regulus andromeda', 'cousin regulus narcissa',
                                'cousin bellatrix sirius', 'cousin bellatrix regulus', 'cousin andromeda sirius',
                                'cousin andromeda regulus', 'cousin narcissa sirius', 'cousin narcissa regulus',
                                'cousin nymphadora draco', 'cousin draco nymphadora']
        black_family_cousins = [
            relation for relation in
            production.forward_chain(family_rules(), data.black_data, verbose=False)
            if "cousin" in relation ]
        if set(black_family_cousins) == set(black_family_cousins_solution):
            self.add_score(5)
        else:
            self.add_message("Incorrect solution for black family cousins")

class Q6(autograder.question.Question):
    def score_question(self, submission):
        # Opus example
        backward_chain = submission.__all__.backchain_to_goal_tree
        answer = "OR('opus is a penguin', AND(OR('opus is a bird', 'opus has feathers', AND('opus flies', 'opus lays eggs')), 'opus does not fly', 'opus swims', 'opus has black and white color'))"

        a = backward_chain(data.zookeeper_rules, 'opus is a penguin')
        if str(a) == answer:
            self.add_score(25)
        else:
            self.add_message("Did not get target tree: %s for hypothesis opus.  Did you simplify the results?"%answer)

def main():
    return autograder.cmd.gradeassignment.main()

if (__name__ == '__main__'):
    sys.exit(main())
