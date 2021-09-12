# Smart Docketing Tool (Updated: 9/11, 10PM ET)
#
# Note: Juvenile Court not included. 
#
# TO DO:
#   - Add appellate court docket-number format, incl. supreme court.
#   - Address local notes
#
# DOCKET-NUMBER FORMATS (STANDARD)
#
#   1.  Superior Court         Example: 1577CV00982
#
#       docket_number[0:1] is the case's filing year 
#       docket_number[2:3] is the court code
#       docket_number[4:5] is the case-type code
#       docket_number[6:10] is the 5-digit sequence number
#
#   2.  District Court         Example: 1670CV000072
#
#       docket_number[0:5] is the same as in the superior-court format.
#       docket_number[6:11] is the 6-digit sequence number
#
#   3.  Boston Municipal Court Example: 1401CV001026
#
#       BMC docket-number format is the same as the district-court format.
#
#   4.  Housing Court          Example: 15H84CV000436
#
#       docket_number[0:1] is the case's filing year 
#       docket_number[2:4] is the court code
#       docket_number[5:6] is the case-type code
#       docket_number[7:12] is the 6-digit sequence number
#
#   5.  Land Court             Example: 07 TL 001026
#
#       LC docket-number format is the same as the district-court format, except
#       without a court code, and the filing year, case-type code, and the
#       6-digit sequence number are each separated by a space.
#
#       NOTE: The subsequent (SBQ) land-court case type, however, has a
#       unique format. Example: 15 SBQ 00025 09-001
#       docket_number[0:6] is the same as in other land-court case types
#       docket_number[7:11] is the 5-digit plan number
#       docket_number[13:14] is the case's filing month
#       docket_number[16:] is the sequence number (likely 3 digits)
#
#   6.  Probate and Family     Example: ES15A0064AD
#
#       docket_number[0:1] is the site or court code
#       docket_number[2:3] is the case's filing year
#       docket_number[4] is the case-group code
#       docket_number[5:8] is the 4-digit sequence number
#       docket_number[9:10] is the case-type code
#
#       I'm not entirely sure what the probate and family court case group adds,
#       as the case type already tells us all the information that the case group
#       would provide. If we can figure out the case group for each case type,
#       this could be used to verify the input docket number. For example, the
#       docket number 'ES00A0000XY' should raise an error, because the docket num-
#       ber tell us that the case TYPE is 'Proxy Guardianship' ('XY') but that
#       the case GROUP is 'Adoption' ('A') instead of 'Proxy Guardianship' ('X').
#
# VARIATIONS
#
#   The format is not a requirement. From one case to another, or even within a
#   the same case, we will see docket numbers that do not follow the above
#   standard formats.
#
#   NOTE: I was able to find uploaded case filings only for superior-court cases,
#   so the list of variations below, except for superior-court variations, assumes
#   that other courts follow similar logic in abbreviating or varying the standard
#   docket-number format. The assumption most definitely stands for district, BMC,
#   and housing courts, as these courts share the same format as superior courts.
#
#   1.  Legend for #2 and #3 lists, below:
#
#       'YY' or 'YYYY'  : 2-digit or 4-digit year, e.g., 21 or 2021
#
#       'CC' or 'hCC'   : 2-character court code, which can be letters only (e.g.,
#                         ES for Essex Probate and Family Ct.), numbers only
#                         (e.g., 77 for Essex Cty. Super. Ct.), or two digits with
#                         prefix 'H' for housing courts. As mentioned, land-court
#                         docket numbers do not have court codes.
#
#       'TT'            : 2-letter case-type code, e.g., CV for Civil, or 2- to 4-
#                         letter case-type code for land court.
#
#       'N'             : Sequence number, e.g., 00001 for the first case in that
#                         court of that year and of that case type. The length
#                         varies between courts and leading 0s are sometimes
#                         removed entirely or all but one.
#
#       'G'             : 1-letter case-group code, applies only to Probate and
#                         Family Ct. 
#
#   2.  Standard formats, using above abbreviations:
#
#       · YYCCTTN+        Super. Ct., Dist. Ct., BMC
#       · YYhCCN+         Housing Ct. Below, I'll just add '/ hCC'
#       · YY TT N+        Land Ct., except SBQ cases
#       · YY SBQ P+ MM-N+ Land Ct., SBQ cases, P is Plan Number, MM is Month
#       · CCYYGN+TT       Probate and Family Court, G is case-group code
#       
#   3.  Variations other than standard format:
#
#       · YYCC-N+ / hCC     Super. Ct., Dist. Ct., BMC / Housing Ct.
#       · YY N+             ALL
#       · YY-N+             ALL
#       · YYYY-N+           ALL
#       · YYCC-N+           ALL
#       · YYCC-TT-N+ / hCC  Super. Ct., Dist. Ct., BMC / Housing Ct.
#       · YY-TT-N+          ALL
#       · YYTTN+            ALL
#       · CCYY-(G)N+        Probate and Family Ct. with or without case-group code
#       · CCTTYY-(G)N+      Probate and Family Ct. with or without case-group code
#
#   4.  Example, variations in practice:
#
#       In SpineFrontier, Inc. v. Cummings Props. LLC, No. 1577CV00982 (Essex Cty.
#       Super. Ct.), in that single case, we see six docket-number variations
#       being used:
#
#           (1) 1577-CV-00982   in the defendant's motion
#           (2) 15-0982         in the defendant's amended counterclaim
#           (3) 15-CV-00982     in the plaintiff's notice of cross-appeal
#           (4) 2015-982        in the court's final-judgment order
#           (5) 2015-00982      in the court's ruling on MSJ
#           (6) 1577CV00982     in the appellate court's notice
#
# LOCAL NOTES
#
#   Local notes are sometimes added to the docket number. For example, in superior
#   courts, civil cases on specific case-management schedules will have the
#   relevant track designations suffixed to the docket number. The three
#   designations are Average Track ('A'), Fast Track ('F'),and Accelerated Track
#   ('X'). There are other local notes, e.g., Business Litigation Session ('BLS').
#   Some courts may include the presiding judge's initials as local notes.
#
#   Only the case-management track designations appear to provide information
#   useful for pro se litigants. The other notes aid clerks of the court.
#
# OTHER CONSIDERATIONS
#
#   Because of the nature and age of the courts' physical stamps, court-stamped
#   documents are unlikely to have standardized docket numbers. This is
#   most relevant at the initial stage of a case, where pro se litigants only
#   have court-stamped civil-action cover sheet returned from the court after
#   filing a case or received from the plaintiff along with the complaint.
#   For example, in Costello v. Needham Bank, the court-stamped civil-action
#   cover sheet has "20 0735" stamped as the docket number. 
#
# ONLINE CASE ACCESS
#
#   Case information and sometimes (rarely, it seems) uploaded PDFs of case
#   filings can be found at masscourts.org.
#
#   Notably (and oddly), the search engine will return with "No Matches Found"
#   if the docket number is not strictly entered in the standardized format,
#   including all the leading 0s.
#
# NOTES ON BELOW CASE-TYPE CODE DICTIONARIES
#
#   The 'AD' case-type code in BMC and district courts refers to 'Appeal' but
#   'Adoption' in probate and family courts. Because of dict key restrictions,
#   the case-type codes for probate and family courts are in a separate dictionary.
#   Land court case-type codes are also in their own dictionary for checking if
#   the docket number is erroneously missing a court code or if the court code
#   is missing because it is a case in the land court.

court_case_type_code_dict = {
    'AC' : 'Application for Criminal Complaint',
    'AD' : 'Appeal',
    'BP' : 'Bail Petition',
    'CI' : 'Civil Infraction',
    'CR' : 'Criminal',
    'CV' : 'Civil',
    'IC' : 'Interstate Compact',
    'IN' : 'Inquest',
    'MH' : 'Mental Health',
    'MV' : 'Motor Vehicle',
    'PC' : 'Probable Cause',
    'RO' : 'Abuse Prevention Order',
    'SC' : 'Small Claims',
    'SP' : 'Supplementary Process',
    'SU' : 'Summary Process',
    'SW' : 'Administrative Search Warrant',
    'TK' : 'Ticket Hearings',
    'PS' : 'Permit Session',
    'SM' : 'Service Members',
    'TL' : 'Tax Lien',
    'REG': 'Registration',
    'SBQ': 'Subsequent',
    'MISC': 'Miscellaneous'
}

land_court_case_type_code_dict = {
    'PS' : 'Permit Session',
    'SM' : 'Service Members',
    'TL' : 'Tax Lien',
    'REG': 'Registration',
    'SBQ': 'Subsequent',
    'MISC': 'Miscellaneous'
}

probate_family_court_case_type_code_dict = {
    'AB' : 'Protection from Abuse',
    'AD' : 'Adoption',
    'CA' : 'Change of Name',
    'CS' : 'Custody, Support, and Parenting Time',
    'CW' : 'Child Welfare',
    'DO' : 'Domestic Relations, Other',
    'DR' : 'Domestic Relations',
    'EA' : 'Estates and Administration',
    'GD' : 'Guardianship',
    'JP' : 'Joint Petition',
    'PE' : 'Paternity in Equity',
    'PM' : 'Probate Abuse / Conservator',
    'PO' : 'Probate, Other',
    'PP' : 'Equity-Partition',
    'QC' : 'Equity Complaint',
    'QP' : 'Equity Petition',
    'SK' : 'Wills for Safekeeping',
    'WD' : 'Paternity',
    'XY' : 'Proxy Guardianship'
}

probate_family_court_case_group_code_dict = {
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

court_name_code_dict = {
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
    'BA' : 'Barnstable Probate and Family Court',
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

import re
import time

find_court_code_re = re.compile(r'(?<=\d{2})(\d{2}|H\d{2})(?=[A-Z](?!$))|'
                                r'^[A-Z]{2}(?=\d)', re.I)
# NEEDS REVISION for variation.
# Match two digits or two digits with prefix 'H' that are preceded by two digits
# and followed by a letter that is not at the end of the string, i.e., not a
# local note. Flag is re.IGNORECASE.
#
# Note land-court docket numbers do not include a court code, and the
# identify_court_name(docket_number) function identifies whether the court is
# land court or not separately from this regular-expression matching.

find_case_type_code_re = re.compile(r'(?<!^)[A-Z]{2,4}', re.I)
# NEEDS REVISION for variation.
# Match two to four letters that are not at the start of the string, i.e., not 
# a probate and family court case.

find_case_year_re = re.compile(r'((?:^)|(?:[A-Z]{2}))\d{2}(?=(?:\d{2}[A-Z]{2})|'
                               r'(?:\s)|(?:-)|(?:[A-Z]+\d)|(?:\d{2}(?:\s|-)))',
                               re.I)
# REVISED to catch variations, except it does not account for YYYY-N+, instead
# assumes that variation is actually YYCC-N+

find_case_sequence_number_re = re.compile(r'\d{2,}(?=$|[A-Z]+$)', re.I)
# Match two or more digits that are at the end of the string or are followed by
# one or more letters (local notes) that are at the end of the string.

check_proper_format_re = re.compile(r'\d{4}[A-Z]{2}\d{1,6}$|'
                                    r'\d{2}H\d{2}[A-Z]{2}\d{1,6}$|'
                                    r'\d{2}\s[A-Z]{2,4}\s\d{1,6}(?:$|\s\d{2}-\d+$)
                                    r'|[A-Z]{2}\d{2}[A-Z]\d+[A-Z]{2}$', re.I)
# REWRITE patterns

def identify_court_name(docket_number):
    court_code = find_court_code_re.search(docket_number).group()
    if not court_code:
        # docket_number is missing court code
        for key in land_court_case_type_code_dict:
            if key in docket_number:
                return 'Land Court'
                # docket_number is missing court code but court is land court
                # and land-court docket numbers do not include court codes so the
                # entered docket_number is still okay
        else:
            return None
            # docket_number is missing court code: the entered docket_number is
            # not okay; this would be where another inquiry and a drop-down menu
            # or a combo-box would be added later for non-standard variations or
            # just incorrectly entered docket numbers. As it is now, because
            # the check_proper_format_re is rigid, this else is unnecessary.
    else:
        if court_code in code_name_code_dict:
            return court_name_code_dict[court_code]
        else:
            return None
            # docket_number has incorrect (not missing) court code

def identify_case_type(docket_number):
    case_type_code = find_case_type_code_re.search(docket_number).group()
    if not case_type_code:
        # docket_number is missing case-type code; input error or variation. As
        # it is now, because the check_proper_format_re is rigid, this is not
        # necessary
        return None
    else:
        court_name = identify_court_name(docket_number)
        if not court_name:
            return None
            # docket_number is missing or has incorrect court code. As it is
            # now, because the check_proper_format_re is rigid, this if not
            # is unnecessary
        elif 'Probate' in court_name:
            for key in probate_family_court_case_type_code_dict:
                if key == case_type_code:
                    return probate_family_court_case_type_code_dict[key]
        else:
            for key in court_case_type_code_dict:
                if key == case_type_code:
                    return court_case_type_code_dict[key]
        
def identify_year(docket_number):
    case_year = find_case_year_re.search(docket_number).group()
    if 'SBQ' in docket_number.upper():
        # .upper() redundant if in input.upper()
        pass # PLACEHOLDER for identifying month and returning month, year
    else:
        if not case_year:
            return None
            # docket_number is missing year
        else:
            if case_year <= time.strftime('%y'):
                return time.strftime('%Y')[:2] + case_year
            else:
                pass # PLACEHOLDER for if identifed year is in the future

def identify_case_sequence_number(docket_number):
    sequence_number = find_case_sequence_number_re.search(docket_number).group()
    if not sequence_number:
        return None
        # docket_number is missing sequence number. As it is now, because
        # check_proper_format_re is rigid, this is unnecessary.
    else:
        return sequence_number

def is_it_in_proper_format(clean_dkt_number):
    if check_proper_format_re.match(clean_dkt_number):
        return True
    else:
        return False

def remove_hyphens_and_spaces(docket_number):
    # First, check if the entered docket number is a land-court docket number,
    # which should have spaces and, in SBQ, a hyphen.
    for key in land_court_case_type_code_dict:
        if key in docket_number.upper():
            if key == 'SBQ':
                # Replace two or more spaces with one space, strip, then remove
                # everything except letters, numbers, spaces, and hyphens, i.e.,
                # all punctuations other than hyphens, and lastly, find all the
                # hyphens and return with list
                remove_extra_spaces = re.sub(r'\s{2,}', ' ',
                                             docket_number).strip()
                remove_punctuations = re.sub(r'[^\w\s-]', '', remove_extra_spaces)
                find_hyphens = re.findall(r'-', remove_punctuations)
                if len(find_hyphens) > 1:
                    # If there are more than one hyphen, remove all except the
                    # hyphen separating month and sequence number
                    extra_hyphen_removed = re.sub(r'-(?!\d+$)','',
                                                  remove_punctuations)
                    clean_dkt_number = extra_hyphen_removed
                    return clean_dkt_number
                elif len(find_hyphens) == 1:
                    clean_dkt_number = remove_punctuations
                    return clean_dkt_number
                else:
                # The hyphen between month and sequence number is missing in SBQ
                # docket number, so add
                add_missing_hyphen = re.sub(r'(?<=\s\d{2})\s(?=\d+$)', '-'
                                            remove_punctuations)
                clean_dkt_number = add_missing_hyphen
                return clean_dkt_number
            else:
                # For other land-court cases, replace two or more spaces with one,
                # strip, then remove everything except letters, numbers, and
                # spaces, i.e., all punctuations
                remove_extra_spaces = re.sub(r'\s{2,}', ' ',
                                             docket_number).strip()
                remove_punctuations = re.sub(r'[^\w\s]', '', remove_extra_spaces)
                clean_dkt_number = remove_punctuations
                return clean_dkt_number
    else:
    # Otherwise, check first whether the input is a docket-number variation with
    # a hyphen or space that separates numbers. In all these variations, the
    # preceding digits are 2- or 4-digits. Sometimes, the two-digit number may
    # be preceded by letter codes. These should not be removed.
        try:
            is_hyphen_space_variation = re.search(r'(?:\d{2,4}|[A-Z]\d{2})'
                                                  r'(-|\s)(?=\d+)',
                                                  docket_number).group(1)
            # If it is a variation, remove all other punctuations and spaces that
            # should not be there
            if is_hyphen_space_variation == '-':
                pass # PLACEHOLDER: write pattern for everything but that hyphen
                     # to remove
            else:
                pass # PLACEHOLDER: write pattern for everything but that space
                     # to remove
        except:
        # If it is not one of those variations, clean up docket number
            remove_non_word_characters = re.sub(r'\W', '', docket_number)
            clean_dkt_number = remove_non_word_characters
            return clean_dkt_number

# For testing:
# docket_number = input('Enter docket number: ')
