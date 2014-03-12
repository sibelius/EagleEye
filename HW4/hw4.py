# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:50:11 2014

@author: xiaohu Nian
 This homework is about probablistic soft logic
"""
""" Store the atom values to the dictionary, with a tuple 
"""
"""
Populate the atom collection, which consist of one interpretation, dictionary 
update the new values automatically  after new assignment
"""
"""represent relationship and predicate
tuples should be in the form of of count, string list, and soft truth value
"""
import math
distance_2 = 0.0
"""
list tag is list of predicate or relationship tag
"""    
list_tag = ['friend','spouse','colleague','vote']
"""
number of entry is the dictionary with predicate as keyword, interger as values to denote the the possible binary, unary, trinary relationship
"""
number_of_entry = {'friend':2, 'spouse':2, 'colleague':2,'vote':2}

list_of_tag_group = dict() #dictionary with tag as keyword, values are a list of tuples
for tag in list_tag:
    list_of_tag_group[tag]=[]
"""
populate the list_of_tag_group
"""
list_of_tag_group['friend']=[('Tom','David', 1),('Emily','Mary',1),('Emily','Lina',1),('Lina','Mary',1),('David','Tom', 1),('Mary','Emily',1),('Lina','Emily',1),('Mary','Lina',1)]
list_of_tag_group['spouse']=[('Tom','Lina', 1),('Lina','Tom',1),('Emily','David',1),('David','Emily',1),('John','Mary',1),('Mary','John',1)]
list_of_tag_group['vote']=[('Tom','Democratic', 1),('Tom','Republic',0),('Lina','Democratic',1),('Lina','Republic',0),('Mary','Democratic',1),('Mary','Republic',0),('David','Republic',1),('David','Democratic',0),('John','Republic',1),('John','Democratic',0)]
list_of_tag_group['colleague']=[('Emily','Tom',1),('Tom','Emily',1),('Emily','John',1),('John','Emily',1)]
"""
specify the rules in the form of list of tuples[(body,head)
After reslove the tag group against rules, we can get each soft logic truth value and then calculate 
"""
rules = [('vote','a','p','and','friend','b','a','infer','vote','b','p'), ('vote','a','p','and','colleague','b','a','infer','vote','b','p'),('vote','a','p','and','spouse','b','a','infer','vote','b','p')]
weights=[0.3,0.2,0.8]   
exponent = 1
weight_index = -1

def find(symbol):
    return number_of_entry[symbol]
def combination_PSL(value_list,operator):
    if operator == 'and':
        return max(0,sum(value_list)-1)
    elif operator == 'or':
        return min(1,sum(value_list))
    else:
        return 1-sum(value_list)
        
def final_calculate(temp_numeric,temp_operator):
    global distance_2
    body = 0.0
    head = 0.0
    one_instance = 0.0
    length_of_temp_operator = len(temp_operator)
    i = 0
    body = combination_PSL(temp_numeric[:2],temp_operator[0])
    flag = 0
    i = 2
    j = 1
    while j < len(temp_operator):
        if temp_operator[j] == 'infer':
            flag = 1
            j = j+1
            if j < length_of_temp_operator-1:
                head = combination_PSL(temp_numeric[i:i+2],temp_operator[j])
            else:
                head = temp_numeric[i]
            i = i+2
            j = j+1
            continue
            
        if flag == 0:
            body =  combination_PSL((body,temp_operator[i]),temp_operator[j])
            i = i+1
            j = j+1
            
        if flag == 1:
            head = combination_PSL((head,temp_operator[i]),temp_operator[j])
            i = i+1
            j = j+1
    """
    print 'distance from satification'
    print max(body-head,0.0)
    one_instance = (-1)*weights[weight_index]*math.pow(max(body-head,0),exponent)
    print 'weight, exponent...weights in'
    print one_instance
    distance_2 = distance_2 + one_instance
    print 'global distance up to'
    print distance_2
    """
    one_instance = weights[weight_index]*math.pow(max(body-head,0),exponent)
    distance_2 = distance_2 + one_instance
    
def reverse_to_old_resolve(old_dict, last_new_symbol_list):
    for symbol in last_new_symbol_list:
        del old_dict[symbol]
    return old_dict            
        
        
        
def further_resolve(pre_resolve, instance, rule, i, k):
    j = 0
    while j < k:
        pre_resolve[rule[i]]=instance[j]
        j = j+1
        i = i+1
    return pre_resolve


def resolve(full_instance, partial_instance):
    length = len(partial_instance)
    i = 0
    while i < length:
        if partial_instance[i] == '*':
            i = i+1
        elif partial_instance[i] != full_instance[i]:
            return False
        else:
            i = i+1
    return True
            
    
def find_partial_instance(predicate,lists,partial_list):
    temp_list = lists[predicate]
    return_list = []
    for element in temp_list:
        if resolve(element,partial_list):
            return_list.append(element)
    return return_list
    
def dis_3(rule,temp_numeric,temp_operator,i,lists,temp_resolve):
    """
    element and i are connected in the way, that rule rule[i] is the predicate of the element
    temp_resolve maps symbol to specific value
    rule are comprised of symbols
    """
    i = i+1
    if i>=len(rule):
        return final_calculate(temp_numeric,temp_operator)
    k = find(rule[i])
    relationship = rule[i]
    j = 0
    partial_list = []
    list_of_new_symbols = []
    i = i+1
    while j < k:
        if rule[i] in temp_resolve:
            partial_list.append(temp_resolve[rule[i]])
            i = i+1
            j = j+1
        else:               
            partial_list.append('*')
            list_of_new_symbols.append(rule[i])
            i = i+1
            j = j+1
    temp_list = find_partial_instance(relationship,lists,partial_list)
    for element_temp_list in temp_list:
        temp_numeric.append(element_temp_list[len(element_temp_list)-1])
        if i<len(rule):
            temp_operator.append(rule[i])
            temp_resolve = further_resolve(temp_resolve, element_temp_list,rule,i-k,k)
            dis_3(rule,temp_numeric,temp_operator,i,lists,temp_resolve)
            del temp_numeric[len(temp_numeric)-1]
            del temp_operator[len(temp_operator)-1]
            temp_resolve = reverse_to_old_resolve(temp_resolve,list_of_new_symbols)
        else:
            dis_3(rule,temp_numeric,temp_operator,i,lists,temp_resolve)
    
                        
""" 
rule     is like ('vote','a' 'b' 'and' 'friend' 'a' 'c' 'infer' 'vote' 'c' 'b')
list    s are all concrete instance of predicate with parameters filled up with specifi value
and the predicate is usually associated with a real value.
Sample element in the list['friend'] is [('Tom','David',1),('Tom','Jakc',0)]
"""    
def dis_2(rule, lists):
    temp_numeric = []
    temp_operator =[]
    k = find(rule[0])
    relationship = rule[0]
    temp_list = lists[relationship]
    temp_resolve = dict()
    for element in temp_list:
        i = 0
        j = 0
        while j < k:
            temp_resolve[rule[j+1]] = element[j]
            j = j+1            
        temp_numeric.append(element[j])
        i = i+k
        i = i+1
        temp_operator.append(rule[i])
        dis_3(rule,temp_numeric,temp_operator,i,lists,temp_resolve)
        temp_resolve=dict()
        temp_numeric=[]
        temp_operator=[]
    
def dis(lists,rules,weights,exponent):
    global weight_index
    global distance_2
    distance_2 = 0.0
    zip_rule_weight = zip(rules, weights)
    for rule_weight in zip_rule_weight:
        weight_index = weight_index + 1
        dis_2(rule_weight[0],lists)
    
"""
question 1 
update the list then run dis
"""
update_step = 0.01
i = -0.01
best_choice = 10000
best_chance = 0.0
while i<=1.0:
    distance_2 = 0.0
    weight_index = -1
    i = i+update_step
    list_of_tag_group['vote'].append(('Emily','Democratic',i))
    list_of_tag_group['vote'].append(('Emily','Republic',1-i))
    dis(list_of_tag_group,rules,weights,exponent)

    print distance_2
    if best_choice > distance_2 :
        best_choice = distance_2
        best_chance = i
    list_of_tag_group['vote'].pop()
    list_of_tag_group['vote'].pop()
    
print 'Emily vote for Democratic'
print 'Best interpretation is'
print best_chance

"""
question 2
update the weight then run dis
"""
list_of_tag_group['vote'].append(('Emily','Democratic',1))
list_of_tag_group['vote'].append(('Emily','Republic',0))

exponent = 1
i = -0.01
j = -0.01
k = -0.01
best_choice = 10000.0
best_chance = 0.0
best_weight = []
while i<=1.0:
    i = i+update_step
    while j<=1.0:
        j = j+update_step
        while k<=1.0:
            k=k+update_step
            weight = [i,j,k]
            weight_index = -1
            distance_2 = 0.0
            dis(list_of_tag_group,rules,weights,exponent)
            if best_choice > distance_2:
                best_weight = weight
                
print 'exponent'
print exponent
print 'best weight'
print best_weight

exponent = 2
i = -0.01
j = -0.01
k = -0.01
best_choice = 10000.0
best_chance = 0.0
best_weight = []
while i<=1.0:
    i = i+update_step
    while j<=1.0:
        j = j+update_step
        while k<=1.0:
            k = k+update_step
            weight = [i,j,k]
            weight_index = -1
            distance_2 = 0.0
            dis(list_of_tag_group,rules,weights,exponent)
            if best_choice > distance_2:
                best_weight = weight
print 'exponent'
print exponent
print 'best weight'
print best_weight
