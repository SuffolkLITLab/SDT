# Smart Docketing Tool
#
# Note: Juvenile Court not included. Also had difficulty accessing case documents
# for courts other than superior court, so possible variations in, e.g., district
# courts are unknown. Still, they are very likely to be similar to superior-court
# variations.
#
# DOCKET-NUMBER FORMAT
#
# 1. Superior Court         Example: 1577CV00982
# docket_number[0:1] is the case's filing year 
# docket_number[2:3] is the court code
# docket_number[4:5] is the case-type code
# docket_number[6:10] is the 5-digit sequence number
#
# 2. District Court         Example: 1670CV000072
# docket_number[0:5] is the same as in the superior-court format.
# docket_number[6:11] is the 6-digit sequence number
#
# 3. Boston Municipal Court Example: 1401CV001026
# BMC docket-number format is the same as the district-court format.
# BMCs and district courts also share the same case-type codes.
#
# 4. Housing Court          Example: 15H84CV000436
# docket_number[0:1] is the case's filing year 
# docket_number[2:4] is the court code
# docket_number[5:6] is the case-type code
# docket_number[7:12] is the 6-digit sequence number
#
# 5. Land Court             Example: 07 TL 001026
# LC docket-number format is the same as the district-court format, except
# LC docket numbers do not have a court code, and the filing year, case-type
# code, and the 6-digit sequence number are each separated by a space.
# The subsequent (SBQ) land-court case type has a unique docket-number format.
# Example: 15 SBQ 00025 09-001.
# docket_number[7:11] is the 5-digit plan number
# docket_number[13:14] is the case's filing month
# docket_number[16:18] is the 3-digit sequence number
#
# 6. Probate and Family     Example: ES15A0064AD
# docket_number[0:1] is the site
# docket_number[2:3] is the case's filing year
# docket_number[4] is the case-group code
# docket_number[5:8] is the 4-digit sequence number
# docket_number[9:10] is the case-type code
#
# VARIATIONS
#
# The format is not a requirement. This can often mean multiple docket-number
# variations in a single case. For example, in SpineFrontier v. Cummings Props.,
# a case in Essex County Superior Court, we see six:
#   (1) 1577-CV-00982   in the defendant's motion
#   (2) 15-0982         in the defendant's amended counterclaim
#   (3) 15-CV-00982     in the plaintiff's notice of cross-appeal
#   (4) 2015-982        in the court's final-judgment order
#   (5) 2015-00982      in the court's ruling on MSJ
#   (6) 1577CV00982     in the appellate court's notice
#
# Observed variations in superior-court cases:
#   1984CV02199     YearCourtTypeSequence   Standard
#   2082-00735      YearCourt-Sequence      
#   1777-1298       YearCourt-Sequence      Excl. leading 0
#   20 0735         Year Sequence           Incl. only one leading 0
#   15-0982         Year-Sequence           Incl. only one leading 0
#   2015-00982      FullYear-Sequence
#   2015-982        FullYear-Sequence       Excl. leading 0
#   1577-CV-00982   YearCourt-Type-Sequence 
#   15-CV-00982     Year-Type-Sequence
#   
# Other possible variations: 21CV01234, 21CV1234, 21-01234, 21-1234
#
# Local notes are sometimes added to the docket number. For example, in superior
# courts, civil cases on specific case-management schedules will have the
# relevant track designations suffixed to the docket number. The three
# designations are Average Track ("A"), Fast Track ("F"),and Accelerated Track
# ("X"). There are other local notes, e.g. Business Litigation Session ("BLS").
#
# OTHER CONSIDERATIONS
#
# Because of the nature and age of the courts' physical stamps,
# court-stamped documents are unlikely to have standardized docket numbers.
# For example, in Costello v. Needham Bank, Suffolk County Superior Court,
# the court-stamped civil-action cover sheet has "20 0735" stamped as the
# docket number. 
# 
# Notably (and oddly), the masscourts.org case search engine will return
# with "No Matches Found" if the docket number is not strictly entered in
# the standardized format, including all the leading 0s.

type_code_dict = {
    'AB' : 'Protection from Abuse',
    'AC' : 'Application for Criminal Complaint',
    'AT' : 'Adoption',      # Actual code is 'AD' but dict restrictions
    'AD' : 'Appeal',        # and determine_type() will still pick up 'Adoption'
    'BP' : 'Bail Petition',
    'CA' : 'Change of Name',
    'CI' : 'Civil Infraction',
    'CR' : 'Criminal',
    'CS' : 'Custody, Support, and Parenting Time',
    'CV' : 'Civil',
    'CW' : 'Child Welfare',
    'DO' : 'Domestic Relations, Other',
    'DR' : 'Domestic Relations',
    'EA' : 'Estates and Administration',
    'GD' : 'Guardianship',
    'IC' : 'Interstate Compact',
    'IN' : 'Inquest',
    'JP' : 'Joint Petition',
    'MH' : 'Mental Health',
    'MV' : 'Motor Vehicle',
    'PC' : 'Probable Cause',
    'PE' : 'Paternity in Equity',
    'PM' : 'Probate Abuse / Conservator',
    'PO' : 'Probate, Other',
    'PP' : 'Equity-Partition',
    'PS' : 'Permit Session',
    'QC' : 'Equity Complaint',
    'QP' : 'Equity Petition',
    'RO' : 'Abuse Prevention Order',
    'SC' : 'Small Claims',
    'SK' : 'Wills for Safekeeping',
    'SM' : 'Service Members',
    'SP' : 'Supplementary Process',
    'SU' : 'Summary Process',
    'SW' : 'Administrative Search Warrant',
    'TK' : 'Ticket Hearings',
    'TL' : 'Tax Lien',
    'WD' : 'Paternity',
    'XY' : 'Proxy Guardianship',
    'REG': 'Registration',
    'SBQ': 'Subsequent',
    'MISC':'Miscellaneous'
}

pf_case_group_code_dict = {
    'A' : 'Adoption',
    'C' : 'Change of Name',
    'D' : 'Domestic Relations',
    'E' : 'Equity',
    'W' : 'Paternity',
    'P' : 'Probate',
    'R' : 'Protection from Abuse',
    'X' : 'Proxy Guardianship',
    'S' : 'Wills for Safekeeping'
}

court_code_dict = {
    '01' : 'Boston Municipal Court (BMC) Central',
    '02' : 'Boston Municipal Court (BMC) Roxbury',
    '03' : 'Boston Municipal Court (BMC) South Boston',
    '04' : 'Boston Municipal Court (BMC) Charlestown',
    '05' : 'Boston Municipal Court (BMC) East Boston',
    '06' : 'Boston Municipal Court (BMC) West Roxbury',
    '07' : 'Boston Municipal Court (BMC) Dorchester',
    '08' : 'Boston Municipal Court (BMC) Brighton',
    '09' : 'Brookline District Court',
    '10' : 'Somerville District Court',
    '11' : 'Lowell District Court',
    '12' : 'Newton District Court',
    '13' : 'Lynn District Court',
    '14' : 'Chelsea District Court',
    '15' : 'Brockton District Court',
    '16' : 'Fitchburg District Court',
    '17' : 'Holyoke District Court',
    '18' : 'Lawrence District Court',
    '20' : 'Chicopee District Court',
    '21' : 'Marlboro District Court',
    '22' : 'Newburyport District Court',
    '23' : 'Springfield District Court',
    '25' : 'Barnstable District Court',
    '26' : 'Orleans District Court',
    '27' : 'Pittsfield District Court',
    '28' : 'Northern Berkshire District Court',
    '29' : 'Southern Berkshire District Court',
    '31' : 'Taunton District Court',
    '32' : 'Fall River District Court',
    '33' : 'New Bedford District Court',
    '34' : 'Attleboro District Court',
    '35' : 'Edgartown District Court',
    '36' : 'Salem District Court',
    '38' : 'Haverhill District Court',
    '39' : 'Gloucester District Court',
    '40' : 'Ipswich District Court',
    '41' : 'Greenfield District Court',
    '42' : 'Orange District Court',
    '43' : 'Palmer District Court',
    '44' : 'Westfield District Court',
    '45' : 'Northampton District Court',
    '47' : 'Concord District Court',
    '48' : 'Ayer District Court',
    '49' : 'Framingham District Court',
    '50' : 'Malden District Court',
    '51' : 'Waltham District Court',
    '52' : 'Cambridge District Court',
    '53' : 'Woburn District Court',
    '54' : 'Dedham District Court',
    '55' : 'Stoughton District Court',
    '56' : 'Quincy District Court',
    '57' : 'Wrentham District Court',
    '58' : 'Hingham District Court',
    '59' : 'Plymouth District Court',
    '60' : 'Wareham District Court',
    '61' : 'Leominster District Court',
    '62' : 'Worcester District Court',
    '63' : 'Gardner District Court',
    '64' : 'Dudley District Court',
    '65' : 'Uxbridge District Court',
    '66' : 'Milford District Court',
    '67' : 'Westborough District Court',
    '68' : 'Clinton District Court',
    '69' : 'East Brookfield District Court',
    '70' : 'Winchendon District Court',
    '72' : 'Barnstable County Superior Court',
    '73' : 'Bristol County Superior Court',
    '74' : 'Dukes County Superior Court',
    '75' : 'Nantucket County Superior Court',
    '76' : 'Berkshire County Superior Court',
    '77' : 'Essex County Superior Court',
    '78' : 'Franklin County Superior Court',
    '79' : 'Hampden County Superior Court',
    '80' : 'Hampshire County Superior Court',
    '81' : 'Middlesex County Superior Court',
    '82' : 'Norfolk County Superior Court',
    '83' : 'Plymouth County Superior Court',
    '84' : 'Suffolk County Superior Court',
    '85' : 'Worcester County Superior Court',
    '86' : 'Peabody District Court',
    '87' : 'Natick District Court',
    '88' : 'Nantucket District Court',
    '89' : 'Falmouth District Court',
    '98' : 'Eastern Hampshire District Court',
    'H77': 'Northeast Housing Court',
    'H79': 'Springfield Housing Court',
    'H83': 'Southeast Housing Court',
    'H84': 'Boston Housing Court',
    'H85': 'Worcester Housing Court',
    'ES' : 'Essex Probate and Family Court',
    'BA' : 'Barnsatble Probate and Family Court',
    'BE' : 'Berkshire Probate and Family Court',
    'BR' : 'Bristol Probate and Family Court',
    'DU' : 'Dukes Probate and Family Court',
    'FR' : 'Franklin Probate and Family Court',
    'HD' : 'Hampden Probate and Family Court',
    'HS' : 'Hampshire Probate and Family Court',
    'MI' : 'Middlesex Probate and Family Court',
    'NA' : 'Nantucket Probate and Family Court',
    'NO' : 'Norfolk Probate and Family Court',
    'PL' : 'Plymouth Probate and Family Court',
    'SU' : 'Suffolk Probate and Family Court',
    'WO' : 'Worcester Probate and Family Court',
}

dept_check_dict = {
    ('BMC', 'District') : ('Application for Criminal Complaint',
                           'Appeal',
                           'Civil',
                           'Civil Infraction',
                           'Criminal',
                           'Interstate Compact',
                           'Inquest',
                           'Mental Health',
                           'Motor Vehicle',
                           'Abuse Prevention Order',
                           'Small Claims',
                           'Supplementary Process',
                           'Administrative Search Warrant'),
    'Superior'          : ('Bail Petition',
                           'Civil',
                           'Criminal'),
    'Housing'           : ('Civil',
                           'Criminal',
                           'Probable Cause',
                           'Small Claims',
                           'Supplementary Process',
                           'Summary Process',
                           'Ticket Hearings'),
    'Land'              : ('Permit Session',
                           'Service Members',
                           'Tax Lien',
                           'Registration',
                           'Subsequent',
                           'Miscellaneous'),
    'Probate'           : ('Adoption',
                           'Protection from Abuse',
                           'Change of Name',
                           'Custody, Support, and Parenting Time',
                           'Child Welfare',
                           'Domestic Relations',
                           'Domestic Relations, Other',
                           'Estates and Administration',
                           'Guardianship',
                           'Joint Petition',
                           'Paternity in Equity',
                           'Probate Abuse / Conservator',
                           'Probate, Other',
                           'Equity-Partition',
                           'Equity Complaint',
                           'Equity Petition',
                           'Wills for Safekeeping',
                           'Paternity',
                           'Proxy')
}

import re
import time

dokt_re = re.compile(r'\d{2}(?=-|\s|[A-Z]{2})|[A-Z]{2}\d{2}', flags = re.I)
type_re = re.compile(r'(?=([A-Z]{2}))', flags = re.I)
tres_re = re.compile(r'(?=([A-Z]{3,}))', flags = re.I)
year_re = re.compile(r'\d{2}(?=\d{2}[A-Z]{2,}\d|[A-Z]\d|-|\s)|'
                     '(?<!\d)\d{2}(?=[A-Z]{2,}\d)|'
                     '(?<![A-Z]\d)\d{2}(?=[A-Z]{2,}\d)', flags = re.I)
                    # '1234CV123', '1234Civ123', '12CV123', 12Civ123', 'CV12-123',
                    # 'CV12 123', '12-123', '12 123', '12H12CV123', 'ES12CV123'
                    # A 'YYYYTypeSeq' docket number, e.g. '2021CV12345'
                    # is highly unlikely, so it's not screened for.
cour_re = re.compile(r'(?<=\w{2})(\d{2}|H\d{2})(?=[A-Z]{2,}(?!$))', flags = re.I)
prob_re = re.compile(r'^[A-Z]{2}(?=\d{2}[A-Z]\d)', flags = re.I)
# Is it possible to do conditional pattern searching with regular expressions?
# prob_re was added because of Probate Court docket numbers: SU21A9999AD
punc_re = re.compile(r'[^A-Z0-9|\s]', flags = re.I)

def choice(udict):
    if len(udict) == 1:
        return udict[1]
    else:
        print('[Which of the following?]')
        for key, value in udict.items():
            print(key, value)
        print('[Choose between 1 and', len(udict),   
              ', 0 if none of the above]', end = ': ')
        while True:
            try:
                select = input().replace(' ','')
                select = int(select)
                # For inputs like '15 ' or '1 5' for 15
                if select == 0:
                    return None
                elif select < 0 or select > len(udict):
                    print('[Please choose between 1 and', len(udict),
                          ' 0 if none of the above]', end = ': ')
                else:
                    break
            except:
                print('[Please enter a numeric value]', end = ': ')
        return udict[select]

def search(user_input, sdict):
    input_dict = {}
    input_list = []
    for comb in user_input:
        for key in sdict:
            if sdict[key] not in input_list:
                if comb.upper() == key:
                    input_list.append(sdict[key])
                elif comb.lower() in sdict[key].lower():
                    input_list.append(sdict[key])
            # For where user inputs abbreviations like 'ad' which could refer
            # to either of the two keys or any of the three values.
            # Avoids duplicates where as key or part of value, it refers to same,
            # e.g. 'ad' matches 'AD' key and 'Adoption' value.
    if input_list:
        input_list.sort()
        for svalue in input_list:
            input_dict[input_list.index(svalue) + 1] = svalue
        choice_result = choice(input_dict)
        return choice_result

def list_filter(flist, fdict):
    flist[:] = list(set(
                [x.lower() for x in flist for key in fdict
                 if x.lower() in key.lower()] +
                [y.lower() for y in flist for key in fdict
                 if y.lower() in fdict[key].lower()]))
    return flist

def y_input(ydict):
    if ydict == type_code_dict:
        dname = 'case type'
        examp = '"CV" or "Civ" for "Civil"'
    else:
        dname = 'court name'
        examp = '"Essex" or just "Ess" for "Essex County Superior Court"'
    att = 3
    que = '[Enter {}, e.g. {}] '.format(dname, examp)
    pro = '[Please try again]'
    while att > 0:
        ans_input = input(que).strip()
        ans_input = punc_re.sub('', ans_input)
        if len(ans_input) > 1:
            #if ans_input.isalpha():
            if ydict == type_code_dict:
                anstype = tres_re.findall(ans_input)
                if not anstype:
                    anstype = type_re.findall(ans_input)
                anstype = list_filter(anstype, type_code_dict)
                testans = search(anstype, type_code_dict)
                if testans is None:
                    att -= 1
                    if att > 0:
                        print('[Try again with different input]')
                else:
                    return testans
                    break
            else:
                ans_input = ans_input.title()
                generic = ['Superior', 'District', 'Housing', 'Probate',
                           'Family', 'Probate and Family', 'Court', 'County',
                           'Sup.', 'Dist.', 'Ct.', 'Cty.', 'Cnty.',
                           'Sup', 'Dist', 'Ct', 'Cty', 'Cnty']
                for gen in generic:
                    ans_input = ans_input.replace(gen, '').strip()
                    # ^^^ is there a better way
                anscour = tres_re.findall(ans_input)
                # ^^^ I'm trying to limit results while at the same time
                # picking up ppl's abbreviations, but can't seem to keep
                # out, for example "Middlesex County Superior Court"
                # if the user enters "Essex" because of the pattern I
                # set, [a-zA-Z]{3}
                if not anscour:
                    anscour = type_re.findall(ans_input)
                anscour = list_filter(anscour, court_code_dict)
                testans = search(anscour, court_code_dict)
                if testans is None:
                    att -= 1
                    if att > 0:
                        print('[Try again with different input]')
                else:
                    return testans
                    break
#            else:
#                att -= 1
#                if att > 0:
#                   print('[Please enter only letters.] \n' + pro)
        else:
            att -= 1
            if att > 0:
                print('[Enter at least 2 characters.] \n' + pro)
    else:
        print('Too many attempts')

def determine_type(dnum):
    for ele in ['REG', 'SBQ', 'MISC']: # Case-type codes with 3+ characters
        if ele in dnum.upper():
            return type_code_dict[ele]
    poten = type_re.findall(dnum)
    poten = list_filter(poten, type_code_dict)
    if not poten:
        print ('[Case-type code is not in the docket number provided]')
        # Provide instructions on where to find case type on document.
        ver_type = input('[Do you see case type? Y/N] ').upper()
        if ver_type in ['Y', 'YE', 'YES']:
            return y_input(type_code_dict)
        else:
            print('[Call for help]')
    else:
        # Test
        return search(poten, type_code_dict)
        
# def sbq_check(sbqnum):

def determine_court(dnum):
    try:
        pfc = prob_re.search(dnum).group()  # Probate and Family Court
        list(pfc)
        return search(pfc)
    except:
        pass
    try:
        otc = cour_re.search(dnum).group()  # Other
        list(otc)
        return search(otc)
    except:
        pcourt = type_re.findall(dnum)
        if not pcourt:
            print('[Court code is not in the docket number provided]')
            # Provide instructions on where to find case type on document.
            ver_court = input('[Do you see court name? Y/N] ').upper()
            if ver_court in ['Y', 'YE', 'YES']:
                return y_input(court_code_dict)
            else:
                print('[Call for help]')
        else:
            # Test
            pcourt = list_filter(pcourt, court_code_dict)
            return search(pcourt, court_code_dict)

def double_check(c_name, t_name):
    for key in dept_check_dict:
        if isinstance(key, tuple):
            for tupkey in key:
                if tupkey in c_name:
                    check_test = dept_check_dict[key]
                    break
        else:
            if key in c_name:
                check_test = dept_check_dict[key]
                break
            else:
                return False
    return t_name in check_test

def determine_year(dnum, ctype):
    pyr = year_re.search(dnum).group()
    if ctype == 'Subsequent':
        print('placeholder') ### add code for month as well
    else:
        if not pyr:
            return 'an unknown year'
        else:
            if pyr <= time.strftime('%y'):
                return time.strftime('%Y')[:2] + pyr

while True:
    docket_number = input('What is the docket number? ')
    if not dokt_re.search(docket_number):
        repeat = input('Code entered in incorrect format. '
                       'Would you like to try again? '
                       'Enter Y/N: ').upper()
        if repeat not in ['Y', 'YE', 'YES']:
            print('Goodbye')
            break
    else:
        case_type = str(determine_type(docket_number))
        court_name = str(determine_court(docket_number))
        case_year = str(determine_year(docket_number, case_type))
        if case_year is None:
            repeat = input('You entered a docket number for a case '
                           'not yet filed. Would you like to try '
                           'with a different docket number? Enter '
                           'Y/N: ').upper()
            if repeat not in ['Y','YE','YES']:
                print('Goodbye')
                break
        elif double_check(court_name, case_type) is True:
            print('why')
        elif double_check(court_name, case_type) is False:
            repeat = input('The {} does not hear {} cases. '.format(
                            court_name, case_type) +
                            'Would you like to try with a different '
                            'docket number? Enter Y/N: ').upper()
            if repeat not in ['Y', 'YE', 'YES']:
                print('Goodbye')
                break
 
        else:
            print('This {} case '.format((case_type).replace('None', 'unknown'))
                  + 'is in {}, '.format((court_name).replace(
                      'None','an unknown court'))
                  + 'and was filed in {}.'.format(case_year))
            break
