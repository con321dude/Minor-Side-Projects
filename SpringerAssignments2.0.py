from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import re
from time import sleep
from secrets import username, pw


file = 'blacklist.txt'

# skips = number of journals to skip (in case last element only has a few classifications, or a problem...)
skips = 0
iterations = 1  # can't be more than the number of journals on the page
pg = 2


"""#Possible update: Error handling, attempt the task repeatedly until no error occurs.
attempt = None
while attempt is None:
    try: attempt = (whatever task)
    except:
     pass

# This does the try function until attempt gets the data correctly. This type of error handling only works when finding data.
"""

"""Possible speed update: Read number of classification matches before continuing, if all sections added up < 50, press cancel and continue the
code with +1 skips"""


def checkName(file, name):
    with open(file, 'r') as read_obj:
        for line in read_obj:
            if name in line:
                return True
    return False


def pickTwoBoardMembers():  # only for use on first page
    count = 0
    x = 0
    totalBoardMembers = 0
    boardMemberTrue = True

    # select two board members
    while (count < 1) and (x < 30):

        criteria = True
        dateLastCompleted = 2021
        dateLastAgreed = 2021

        try:
            current = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_CurrentDataRow_'+'{x}'.format(x=x))
        except:
            # no more reviewers on this page!
            # print("Not enough reviewers on this article... ")

            return

        while criteria != False:
            # Check if board member:
            boardMember = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_CurrentDataRow_'+'{x}'.format(x=x)).text

            # print("\n\nBoard Member: ", boardMember)

            if ("Yes" in boardMember):
                # print("This is a board member.")

                if("Author" in boardMember):
                    # print("This is the author... skipping")
                    x += 1
                    criteria = False
                    break

            else:
                # print("Not a board member, exiting...")
                x += 1
                criteria = False
                break

            # c = input("Temporary break: ")

            # Check peoplenotes
            peoplenotes = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_InternalNamePanel_'+'{x}'.format(x=x)).text
            # print("Peoplenotes = ", peoplenotes)
            if ("☢" in peoplenotes):

                # print("Reviewer opted out... skipping")
                x += 1
                criteria = False
                break

            # c = input("Break")

            # Check publicationInfo
            publicationInfo = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_InternalReviewerData_'+'{x}'.format(x=x)).text
            # print(publicationInfo)
            # c = input("Break")
            if ("Reviewer Declined" in publicationInfo):
                # print("Reviewer has already declined this article... skipping")
                x += 1
                criteria = False
                break
            elif("Un-invited" in publicationInfo):
                # print("Reviewer has been un-invited... skipping")
                x += 1
                criteria = False
                break
            elif("Complete" in publicationInfo):
                # print("Reviewer has already completed a review... skipping")
                x += 1
                criteria = False
                break

            # Check Name
            name = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_ReviewerNameLink_'+'{x}'.format(x=x)).text

            # print("\n\nReviewer", x+1, " Name: ", name)

            # if name belongs to the blacklist:
            if (checkName(file, name) == True):
                # print("This reviewer belongs to the 'blacklist.txt' file, so will not be assigned!")
                x += 1
                criteria = False
                break

            # Check Reviews in Progress
            reviewsInProgress = int(driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_ReviewerStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[1]/td[2]').text)

            # print("Reviews in progress: ", reviewsInProgress)

            if reviewsInProgress > 5:
                # print("Too many reviews in progress!")
                x += 1
                criteria = False
                break

            # Check Outstanding Invitations
            outstandingInvitations = int(driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_InvitationStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[2]/td[2]').text)

            # print("Outstanding Invitations: ", outstandingInvitations)

            # c = input("break")

            if outstandingInvitations > 3:
                # print("Too many Outstanding Invitations!")
                x += 1
                criteria = False
                break

            # Check Date last completed
            fullDateLastCompleted = driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_ReviewerStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[6]/td[2]').text
            # print("Last Review Completed: ", fullDateLastCompleted)

            if fullDateLastCompleted != "-               ":
                # first four digits of the date = the Year
                dateLastCompleted = int(fullDateLastCompleted[0:4])

                # print("Last Review Completed (Year only): ", dateLastCompleted)
                if dateLastCompleted < 2018:
                    # print("\nDate last completed was before 2018!")
                    x += 1
                    criteria = False
                    break

            elif fullDateLastCompleted == "-               ":  # no completions
                dateLastCompleted = "-"
                # print("Last Review Completed (Year only): ", dateLastCompleted)
                lottery = random.randint(0, 30)
                # print("Random number 1 to 30 is:", lottery)
                if lottery != 1:
                    # print("This person has no completions, skipping this reviewer...")
                    x += 1
                    criteria = False
                    break
                # else:
                    # print(
                    # "This person has no completions, but randomly got selected to continue the criteria check!")

                    # Check Date last agreed
            fullDateLastAgreed = driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_ReviewerStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[5]/td[2]').text

            # print("Last Review Agreed: ", fullDateLastAgreed)

            if fullDateLastAgreed != "-               ":
                # first four digits of the date = the Year
                dateLastAgreed = int(fullDateLastAgreed[0:4])

                # print("Last Review Agreed: ", fullDateLastAgreed)
                # print("Last Review Agreed (Year only): ", dateLastAgreed)
                if dateLastAgreed < 2018:
                    # print("\nDate last agreed was before 2018!")
                    x += 1
                    criteria = False
                    break

            elif fullDateLastAgreed == "-               ":  # no completions
                dateLastAgreed = "-"
                # print("Last Review Agreed: ", fullDateLastAgreed)
                # print("Last Review Agreed (Year only): ", dateLastAgreed)
                lottery = random.randint(0, 30)
                # print("Random number 1 to 30 is:", lottery)
                if lottery != 1:
                    # print("This person has no completions, skipping this reviewer...")
                    x += 1
                    criteria = False
                    break
                # else:
                    # print("This person has no completions, but randomly got selected to continue the criteria check!")

                    # Check agree amount
            agreed = int(driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_InvitationStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[3]/td[2]').text)

            # print("Agreed: ", agreed)

            # Check decline amount
            declined = int(driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_InvitationStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[4]/td[2]').text)

            # print("Declined: ", declined)

            # calculate agree/disagree ratio

            if declined <= 10:  # if they havent declined enough any yet, give them a chance!
                declined = 1
                agreed = 1

            ratio = agreed/declined
            if (ratio < 0.1):
                # print("Agree : Disagree ratio too low!")
                x += 1
                criteria = False
                break

            # check other stuff:

            # if name has already been used for this article:
            if (driver.find_element_by_id(
                    'ReviewersGrid_ReviewersGridRepeater_InvitedBox_'+'{x}'.format(x=x)).is_selected()):
                # print("This reviewer has already been checked!")
                x += 1
                criteria = False
                break

            # Reached end of criteria check: assign this reviewer
            reviewersAssigned.append(current)
            driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_InvitedBox_'+'{x}'.format(x=x)).click()
            # print("This reviewer has been checked!")

            count += 1
            x += 1
            # print("Count = ", count)
            # print("x = ", x)

            criteria = False  # End of loop for this reviewer, go to next


def pickNonBoardMembers():
    count = 0
    x = 0

    usedPages = []

    pageSummary = str(driver.find_element_by_id("ReviewersGrid_TopPaginator_paginatorSummary").text)

    # print("pageSummary=", pageSummary)

    currentPage = int(pageSummary.split()[1])

    # print("Current page = ", currentPage)

    totalPages = int(pageSummary.split()[3])
    # print("Total pages = ", totalPages)

    usedPages.append(currentPage)

    # print("usedPages = ", usedPages)

    #c = input("Break")

    while (count < 24):

        criteria = True
        dateLastCompleted = 2020
        dateLastAgreed = 2020
        minimumReviewers = 15

        try:  # attempts to get the next reviewer
            current = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_CurrentDataRow_'+'{x}'.format(x=x))

        except:  # Reached end of page before getting max reviewers

            # print("Reached end of page before getting enough reviewers... ")

            x = 0

            if len(usedPages) == totalPages:  # we have used all the pages already!!

                    # if all pages have been used:
                print("number of reviewers selected = ", count)
                # print("Not enough reviewers on this article... increasing skips and going back to new assignments.")
                # click cancel Button
                if count > minimumReviewers:
                    print("We have enough reviewers, proceeding with this many...")
                else:
                    driver.find_element_by_id("CancelButton").click()
                # this should now exit the pickreviewers()...
                # c = input("Break, this should now exit the pickreviewers()...")

                return
            else:

                # print("Going to new page that hasn't been used yet...")
                # print("All the used pages so far: ", usedPages)
                # print("Length of usedPages: ", len(usedPages))

                try:  # attempt to go to next page
                    # print("Moving on to the next page")

                    driver.find_element_by_id(
                        "ReviewersGrid_TopPaginator_GoToNext").click()

                    # print("New page has been clicked...")

                    time.sleep(6)

                    pageSummary = str(driver.find_element_by_id(
                        "ReviewersGrid_TopPaginator_paginatorSummary").text)
                    # print("pageSummary=", pageSummary)

                    currentPage = int(pageSummary.split()[1])
                    # print("Current page = ", currentPage)

                    totalPages = int(pageSummary.split()[3])
                    # print("Total pages = ", totalPages)

                    usedPages.append(currentPage)
                    # print("usedPages = ", usedPages)

                except:  # we are on the last page, go back to first page
                    # print("We are on the last page, but haven't used all pages, going back to first page...")
                    driver.find_element_by_id("ReviewersGrid_TopPaginator_GoToFirst").click()

                    pageSummary = str(driver.find_element_by_id(
                        "ReviewersGrid_TopPaginator_paginatorSummary").text)
                    # print("pageSummary=", pageSummary)

                    currentPage = int(pageSummary.split()[1])
                    # print("Current page = ", currentPage)

                    totalPages = int(pageSummary.split()[3])
                    print("Total pages = ", totalPages)

                    usedPages.append(currentPage)
                    # print("usedPages = ", usedPages)

                    time.sleep(5)

        while criteria != False:
            # Make sure its not a board member:

            boardMember = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_CurrentDataRow_'+'{x}'.format(x=x)).text

            # print("\n\nBoard Member: ", boardMember)

            if ("Yes" in boardMember):
                # print("This is a board member, skipping...")
                x += 1
                criteria = False
                break

            elif("Author" in boardMember):
                # print("This is the author... skipping")
                x += 1
                criteria = False
                break

            # else:
                # print("Not a board member, continuing...")

                # Check Name
            name = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_ReviewerNameLink_'+'{x}'.format(x=x)).text

            # print("\n\nReviewer", x+1, " Name: ", name)

            # if name belongs to the blacklist:
            if (checkName(file, name) == True):
                # print("This reviewer belongs to the 'blacklist.txt' file, so will not be assigned!")
                x += 1
                criteria = False
                break

            # Check peoplenotes
            peoplenotes = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_InternalNamePanel_'+'{x}'.format(x=x)).text
            # print("Peoplenotes = ", peoplenotes)
            if ("☢" in peoplenotes):

                # print("Reviewer opted out... skipping")
                x += 1
                criteria = False
                break

            # c = input("Break")

            # Check publicationInfo
            publicationInfo = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_InternalReviewerData_'+'{x}'.format(x=x)).text
            # print(publicationInfo)
            # c = input("Break")
            if ("Reviewer Declined" in publicationInfo):
                # print("Reviewer has already declined this article... skipping")
                x += 1
                criteria = False
                break
            elif("Un-invited" in publicationInfo):
                # print("Reviewer has been un-invited... skipping")
                x += 1
                criteria = False
                break
            elif("Complete" in publicationInfo):
                # print("Reviewer has already completed a review... skipping")
                x += 1
                criteria = False
                break

            # Check Reviews in Progress
            reviewsInProgress = int(driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_ReviewerStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[1]/td[2]').text)

            # print("Reviews in progress: ", reviewsInProgress)

            if reviewsInProgress > 5:
                # print("Too many reviews in progress!")
                x += 1
                criteria = False
                break

            # Check Outstanding Invitations
            outstandingInvitations = int(driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_InvitationStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[2]/td[2]').text)

            # print("Outstanding Invitations: ", outstandingInvitations)
            # c = input("break")

            if outstandingInvitations > 3:
                # print("Too many Outstanding Invitations!")
                x += 1
                criteria = False
                break

            # Check Date last completed
            fullDateLastCompleted = driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_ReviewerStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[6]/td[2]').text
            # print("Last Review Completed: ", fullDateLastCompleted)

            if fullDateLastCompleted != "-               ":
                # first four digits of the date = the Year
                dateLastCompleted = int(fullDateLastCompleted[0:4])

                # print("Last Review Completed (Year only): ", dateLastCompleted)
                if dateLastCompleted < 2018:
                    # print("\nDate last completed was before 2018!")
                    x += 1
                    criteria = False
                    break

            elif fullDateLastCompleted == "-               ":  # no completions
                dateLastCompleted = "-"
                # print("Last Review Completed (Year only): ", dateLastCompleted)
                lottery = random.randint(0, 30)
                # print("Random number 1 to 30 is:", lottery)
                if lottery != 1:
                    # print("This person has no completions, skipping this reviewer...")
                    x += 1
                    criteria = False
                    break
                # else:
                    # print(
                    #     "This person has no completions, but randomly got selected to continue the criteria check!")

                    # Check Date last agreed
            fullDateLastAgreed = driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_ReviewerStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[5]/td[2]').text

            # print("Last Review Agreed: ", fullDateLastAgreed)

            if fullDateLastAgreed != "-               ":
                # first four digits of the date = the Year
                dateLastAgreed = int(fullDateLastAgreed[0:4])

                # print("Last Review Agreed: ", fullDateLastAgreed)
                # print("Last Review Agreed (Year only): ", dateLastAgreed)
                if dateLastAgreed < 2018:
                    # print("\nDate last agreed was before 2018!")
                    x += 1
                    criteria = False
                    break

            elif fullDateLastAgreed == "-               ":  # no completions
                dateLastAgreed = "-"
                # print("Last Review Agreed: ", fullDateLastAgreed)
                # print("Last Review Agreed (Year only): ", dateLastAgreed)
                lottery = random.randint(0, 30)
                # print("Random number 1 to 30 is:", lottery)
                if lottery != 1:
                    # print("This person has no completions, skipping this reviewer...")
                    x += 1
                    criteria = False
                    break
                # else:
                    # print(
                    #     "This person has no completions, but randomly got selected to continue the criteria check!")

                    # Check agree amount
            agreed = int(driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_InvitationStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[3]/td[2]').text)

            # print("Agreed: ", agreed)

            # Check decline amount
            declined = int(driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_InvitationStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[4]/td[2]').text)

            # print("Declined: ", declined)

            # calculate agree/disagree ratio

            if declined < 10:  # if they havent declined any yet, give them a chance!
                declined = 1
                agreed = 1

            ratio = agreed/declined
            if (ratio < 0.1):
                # print("Agree : Disagree ratio too low!")
                x += 1
                criteria = False
                break

            # check other stuff:

            # if name has already been used for this article:
            try:
                if (driver.find_element_by_id(
                    'ReviewersGrid_ReviewersGridRepeater_InvitedBox_'+'{x}'.format(x=x)).is_selected()):
                # print("This reviewer has already been checked!")
                    x += 1
                    criteria = False
                    break
            except:
                x+=1
                criteria = False
                break

            # Reached end of criteria check: assign this reviewer
            try:
                driver.find_element_by_id(
                    'ReviewersGrid_ReviewersGridRepeater_InvitedBox_'+'{x}'.format(x=x)).click()
                reviewersAssigned.append(current)
                count +=1
                x += 1
            except:
                print("unable to select this reviewer")
            # print("This reviewer has been checked!")
                x += 1
            # print("Count = ", count)
            # print("x = ", x)

            criteria = False  # End of loop for this reviewer, go to next


def pick22NonBoardMembers():

    #c = input("start")
    count = 0
    x = 0

    usedPages = []

    pageSummary = str(driver.find_element_by_id(
        "ReviewersGrid_TopPaginator_paginatorSummary").text)

    # print("pageSummary=", pageSummary)

    currentPage = int(pageSummary.split()[1])

    # print("Current page = ", currentPage)

    totalPages = int(pageSummary.split()[3])
    # print("Total pages = ", totalPages)

    usedPages.append(currentPage)

    # print("usedPages = ", usedPages)
    # c = input("break")

    while (count < 16):  # or (x < len(reviewers)-1) or (x < 99):
        criteria = True
        dateLastCompleted = 2020
        dateLastAgreed = 2020
        minimumReviewers = 10

        try:

            current = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_CurrentDataRow_'+'{x}'.format(x=x))
        except:
            x = 0

            # print("Reached end of page before getting enough reviewers... ")

            if len(usedPages) == totalPages:  # we have used all the pages already!!
                print("number of reviewers selected = ", count)
                # c = input("all pages used, finished.")

                    # if all pages have been used:

                # print(
                #     "Not enough reviewers on this article... increasing skips and going back to new assignments.")
                # click cancel Button

                if count > minimumReviewers:
                    print("We have enough reviewers, proceeding with this many...")
                else:
                    driver.find_element_by_id("CancelButton").click()

                # this should now exit the pickreviewers()...
                # c = input("Break, this should now exit the pickreviewers()...")

                return
            else:

                # print("Going to new page that hasn't been used yet...")
                # print("All the used pages so far: ", usedPages)
                # print("Length of usedPages: ", len(usedPages))

                try:  # attempt to go to next page
                    # print("Moving on to the next page")

                    driver.find_element_by_id(
                        "ReviewersGrid_TopPaginator_GoToNext").click()

                    # print("New page has been clicked...")

                    time.sleep(6)

                    pageSummary = str(driver.find_element_by_id(
                        "ReviewersGrid_TopPaginator_paginatorSummary").text)
                    # print("pageSummary=", pageSummary)

                    currentPage = int(pageSummary.split()[1])
                    # print("Current page = ", currentPage)

                    totalPages = int(pageSummary.split()[3])
                    # print("Total pages = ", totalPages)

                    usedPages.append(currentPage)
                    print("usedPages = ", usedPages)
                    # c = input("break")

                except:  # we are on the last page, go back to first page
                    # print(
                    #     "We are on the last page, but haven't used all pages, going back to first page...")
                    driver.find_element_by_id(
                        "ReviewersGrid_TopPaginator_GoToFirst").click()

                    pageSummary = str(driver.find_element_by_id(
                        "ReviewersGrid_TopPaginator_paginatorSummary").text)
                    # print("pageSummary=", pageSummary)

                    currentPage = int(pageSummary.split()[1])
                    # print("Current page = ", currentPage)

                    totalPages = int(pageSummary.split()[3])
                    # print("Total pages = ", totalPages)

                    usedPages.append(currentPage)
                    # print("usedPages = ", usedPages)

                    time.sleep(5)

        criteria = True
        while criteria != False:
            # Make sure its not a board member:

            boardMember = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_CurrentDataRow_'+'{x}'.format(x=x)).text

            # print("\n\nBoard Member: ", boardMember)

            if ("Yes" in boardMember):
                # print("This is a board member, skipping...")
                x += 1
                criteria = False
                break

            elif("This is the Corresponding Author of the manuscript." in boardMember):
                # print("This is the author... skipping")
                x += 1
                criteria = False
                break

            # else:
                # print("Not a board member, continuing...")

                # Check Name
            name = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_ReviewerNameLink_'+'{x}'.format(x=x)).text

            # print("\n\nReviewer", x+1, " Name: ", name)

            # if name belongs to the blacklist:
            if (checkName(file, name) == True):
                # print("This reviewer belongs to the 'blacklist.txt' file, so will not be assigned!")
                x += 1
                criteria = False
                break

            # Check peoplenotes
            peoplenotes = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_InternalNamePanel_'+'{x}'.format(x=x)).text
            # print("Peoplenotes = ", peoplenotes)
            if ("☢" in peoplenotes):

                # print("Reviewer opted out... skipping")
                x += 1
                criteria = False
                break

            # c = input("Break")

            # Check publicationInfo
            publicationInfo = driver.find_element_by_id(
                'ReviewersGrid_ReviewersGridRepeater_InternalReviewerData_'+'{x}'.format(x=x)).text

            # print(publicationInfo)
            # c = input("Break")
            if ("Reviewer Declined" in publicationInfo):
                # print("Reviewer has already declined this article... skipping")
                x += 1
                criteria = False
                break
            elif("Un-invited" in publicationInfo):
                # print("Reviewer has been un-invited... skipping")
                x += 1
                criteria = False
                break
            elif("Complete" in publicationInfo):
                # print("Reviewer has already completed a review... skipping")
                x += 1
                criteria = False
                break

            # Check Reviews in Progress
            reviewsInProgress = int(driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_ReviewerStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[1]/td[2]').text)

            # print("Reviews in progress: ", reviewsInProgress)

            if reviewsInProgress > 5:
                # print("Too many reviews in progress!")
                x += 1
                criteria = False
                break

            # Check Outstanding Invitations
            outstandingInvitations = int(driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_InvitationStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[2]/td[2]').text)

            # print("Outstanding Invitations: ", outstandingInvitations)
            # c = input("break")

            if outstandingInvitations > 3:
                # print("Too many Outstanding Invitations!")
                x += 1
                criteria = False
                break

            # Check Date last completed
            fullDateLastCompleted = driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_ReviewerStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[6]/td[2]').text
            # print("Last Review Completed: ", fullDateLastCompleted)

            if fullDateLastCompleted != "-               ":
                # first four digits of the date = the Year
                dateLastCompleted = int(fullDateLastCompleted[0:4])

                # print("Last Review Completed (Year only): ", dateLastCompleted)
                if dateLastCompleted < 2018:
                    # print("\nDate last completed was before 2018!")
                    x += 1
                    criteria = False
                    break

            elif fullDateLastCompleted == "-               ":  # no completions
                dateLastCompleted = "-"
                # print("Last Review Completed (Year only): ", dateLastCompleted)
                lottery = random.randint(0, 30)
                # print("Random number 1 to 30 is:", lottery)
                if lottery != 1:
                    # print("This person has no completions, skipping this reviewer...")
                    x += 1
                    criteria = False
                    break
                # else:
                    # print(
                    #     "This person has no completions, but randomly got selected to continue the criteria check!")

                    # Check Date last agreed
            fullDateLastAgreed = driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_ReviewerStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[5]/td[2]').text

            # print("Last Review Agreed: ", fullDateLastAgreed)

            if fullDateLastAgreed != "-               ":
                # first four digits of the date = the Year
                dateLastAgreed = int(fullDateLastAgreed[0:4])

                # print("Last Review Agreed: ", fullDateLastAgreed)
                # print("Last Review Agreed (Year only): ", dateLastAgreed)
                if dateLastAgreed < 2018:
                    # print("\nDate last agreed was before 2018!")
                    x += 1
                    criteria = False
                    break

            elif fullDateLastAgreed == "-               ":  # no completions
                dateLastAgreed = "-"
                # print("Last Review Agreed: ", fullDateLastAgreed)
                # print("Last Review Agreed (Year only): ", dateLastAgreed)
                lottery = random.randint(0, 30)
                # print("Random number 1 to 30 is:", lottery)
                if lottery != 1:
                    # print("This person has no completions, skipping this reviewer...")
                    x += 1
                    criteria = False
                    break
                # else:
                    # print(
                    #     "This person has no completions, but randomly got selected to continue the criteria check!")

                    # Check agree amount
            agreed = int(driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_InvitationStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[3]/td[2]').text)

            # print("Agreed: ", agreed)

            # Check decline amount
            declined = int(driver.find_element_by_xpath(
                '//*[@id="ReviewersGrid_ReviewersGridRepeater_InvitationStatisticsCell_'+'{x}'.format(x=x)+'"]/table/tbody/tr[4]/td[2]').text)

            # print("Declined: ", declined)

            # calculate agree/disagree ratio

            if declined < 10:  # if they havent declined any yet, give them a chance!
                declined = 1
                agreed = 1

            ratio = agreed/declined
            if (ratio < 0.1):
                # print("Agree : Disagree ratio too low!")
                x += 1
                criteria = False
                break

            # if this person has already been used for this article: (must be last because if it doesn't exist then it wont find the checkbox and output an error)
            if (driver.find_element_by_id(
                    'ReviewersGrid_ReviewersGridRepeater_InvitedBox_'+'{x}'.format(x=x)).is_selected()):
                # print("This reviewer has already been checked!")
                x += 1
                criteria = False
                break

            # check other stuff:

            # Reached end of criteria check: assign this reviewer

            try:
                print("Selecting this reviewer")
                driver.find_element_by_id(
                    'ReviewersGrid_ReviewersGridRepeater_InvitedBox_'+'{x}'.format(x=x)).click()
                # print("This reviewer has already been checked!")
                reviewersAssigned.append(current) #add the reviewer to the list of used reviewers
                count+=1
                x += 1
                criteria = False
                break
            except:
                print("unable to click this box, going to next reviewer")
                x+=1
                criteria = False
                break

            # print("This reviewer has been checked!")

            if(criteria == False):
                print("reached end of criteria check but criteria == false")

                break



            # print("Count = ", count)
            # print("x = ", x)

            criteria = False  # End of loop for this reviewer, go to next
            print("next reviewer")
            break


    print("number of reviewers selected = ", count)

    # c=input("finished selecting.")

# Load Web Page
# print("Loading EditorialManager...")
driver = webdriver.Chrome(executable_path="./chromedriver.exe")

# "C:/Users/chammock2015/Desktop/Work/Editor Assigning Algorithm/chromedriver.exe"
# C:/chromedriver_win32/chromedriver.exe"

driver.get('https://www.editorialmanager.com/mtap/default.aspx')

# print("Maximizing Window...")
driver.maximize_window()

# driver.implicitly_wait(3) #Wait until page loads


window_before = driver.window_handles[0]

# for handle in driver.window_handles:
#     print(handle)


delay = 0.1

frame = WebDriverWait(driver, delay).until(
    EC.presence_of_element_located((By.XPATH, '//frame[@name="content"]')))

# Access the frame which has the login box

# frame = driver.find_element_by_xpath('//frame[@name="content"]')
time.sleep(1)
driver.switch_to.frame(frame)
iframe = driver.find_element_by_xpath('//iframe[@name="login"]')
driver.switch_to.frame(iframe)

# c = input("Input any key to continue: ")  # Temporary manual breakpoint


# Input username and password
# print("Inputting credentials from 'secrets.py' ...")

driver.find_element_by_id('username').send_keys(username)
driver.find_element_by_id('passwordTextbox').send_keys(pw)

# c = input("Input any key to continue: ")  # Temporary manual breakpoint

# click Editor Login button
# print("Logging in...")
driver.find_element_by_xpath(
    '/html/body/div/div[2]/form/div/fieldset/table/tbody/tr[1]/td/div/div[1]/input[3]').click()


# wait for window to change
time.sleep(6)

# WebDriverWait(driver, 10).until(lambda d: d.title != "")

# Refresh window and frame

# for handle in driver.window_handles:
#     print(handle)

# Before:CDwindow-277BD459233E9A37467643DEA69E5CD9
# After: CDwindow-277BD459233E9A37467643DEA69E5CD9


window = driver.window_handles[0]
driver.switch_to.window(window)
frame = driver.find_element_by_xpath('//frame[@name="content"]')
driver.switch_to.frame(frame)

# c = input("Input any key to continue: ")  # Temporary manual breakpoint
option = int(input(
    "What would you like to do? \n 1. New assignments \n 2. Submissions Requiring Additional Reviewers \n"))

if option == 1:
    iterations = 0
    total = int(input("How many iterations?  \n"))
    # Click New Assignments button
    # print("Selecting 'New Assignments' ...")
    driver.find_element_by_xpath(
        '/html/body/form/div[3]/div[3]/div/div/div[3]/fieldset/div/div[1]/a[1]').click()

    # Refresh Window and Frame
    time.sleep(3)

    window = driver.window_handles[0]
    driver.switch_to.window(window)
    frame = driver.find_element_by_xpath('//frame[@name="content"]')
    driver.switch_to.frame(frame)

    # Click double arrow to go to last page
    button = driver.find_element_by_xpath(
        "//table[@id='datatable']//tr[last()-"+'{x}'.format(x=skips)+"]")
    # ActionChains(driver).move_to_element(button).click(button).perform()
    articleNum = str(button.get_attribute('id'))
    decision = driver.find_element_by_id("n"+'{x}'.format(x=articleNum))
    # sort by Editor Decision to avoid Major/Minor Revisions

    if("Major Revision" in decision.text):
        driver.find_element_by_xpath(
            '//*[@id="FGSubmissions"]/div[3]/div[1]/div[2]/div[2]/div[1]/table/thead/tr/th[9]/div/div/div[1]/div[1]/a').click()
        time.sleep(6)
    elif("Minor Revision" in decision.text):
        driver.find_element_by_xpath(
            '//*[@id="FGSubmissions"]/div[3]/div[1]/div[2]/div[2]/div[1]/table/thead/tr/th[9]/div/div/div[1]/div[1]/a').click()
        time.sleep(6)
    else:
        pass

    # pause:
    window = driver.window_handles[0]
    driver.switch_to.window(window)
    frame = driver.find_element_by_xpath('//frame[@name="content"]')
    driver.switch_to.frame(frame)

    decision = driver.find_element_by_id("n"+'{x}'.format(x=articleNum))

    # c = input("Input any key to continue: ")  # Temporary manual breakpoint

    """driver.find_element_by_class_name('fg-page-last').click()"""

    # c = input("Input any key to continue: ")  # Temporary manual breakpoint

    # skips = int(input("How many skips? ")) #no longer needed!!
    skips = 0

    # start of loop:
    while total != 0:
        if skips <= 100:
            # Refresh Window and Frame
            time.sleep(6)
            window = driver.window_handles[0]
            driver.switch_to.window(window)
            frame = driver.find_element_by_xpath('//frame[@name="content"]')
            driver.switch_to.frame(frame)

            # c = input("Input any key to continue: ")  # Temporary manual breakpoint
            check = False
            while(check == False):
                # Select LAST Invite Reviewers button on the executable_path
                # print("Selecting last 'Invite Reviewers option' ...")
                button = driver.find_element_by_id(
                    "fr"+'{x}'.format(x=skips))  # last()- //*[@id="fr0"]
                ActionChains(driver).move_to_element(button).click(button).perform()

                # print(button.get_attribute('id'))

                articleNum = str(button.get_attribute('id'))
                decision = driver.find_element_by_id("n"+'{x}'.format(x=articleNum))

                # print(decision.text)
                #c = input("break")

                # since we sort by revisions, if we reach a major/minor revision, we can assume the rest will all be the same so we exit.
                if("Major Revision" in decision.text):
                    print("Editor Decision contains a 'Revision'. You must have completed all possible non-revisions. The total amount you completed is: ", iterations)
                    c = input(
                        "This is a final exit breakpoint, exit the code here after writing down 'iterations'!")
                elif("Minor Revision" in decision.text):
                    print("Editor Decision contains a 'Revision'. You must have completed all possible non-revisions. The total amount you completed is: ", iterations)
                    c = input(
                        "This is a final exit breakpoint, exit the code here after writing down 'iterations'!")

                elif ("Accept as is" in decision.text):
                    # print("Editor Decision contains a 'Accept as is'. Increasing skips...")
                    if(articleNum == "fr100"):
                        # print("All articles on this page are skips, going forward a page... and keeping the skips")

                        driver.find_element_by_xpath(
                            '//*[@id="FGSubmissions"]/div[3]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[2]/table/tbody/tr/td[4]/a').click()
                        # /html/body/form/div[4]/div[3]/div/div[3]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[2]/table/tbody/tr/td[4]/a
                        time.sleep(6)
                        window = driver.window_handles[0]
                        driver.switch_to.window(window)
                        frame = driver.find_element_by_xpath('//frame[@name="content"]')
                        driver.switch_to.frame(frame)
                    skips += 1

                else:
                    # print("This article works, choosing this one: ", articleNum)
                    if(articleNum == "fr100"):
                        lastArticle = True

                    check = True

            button.find_element_by_link_text("Invite Reviewers").click()

            # Refresh Window and frame
            time.sleep(3)
            window = driver.window_handles[0]
            driver.switch_to.window(window)
            frame = driver.find_element_by_xpath('//frame[@name="content"]')
            driver.switch_to.frame(frame)

            # c = input("Input any key to continue: ")  # Temporary manual breakpoint

            # print("Searching by Classification Matches...")
            driver.find_element_by_xpath(
                "//select[@name='ReviewerSearchOptions$HomeJournalSearchModeDropDown']/option[text()='Search by Classification Matches']").click()

            driver.find_element_by_xpath(
                '/html/body/div[1]/form/div[4]/div[3]/fieldset/table/tbody/tr/td[5]/input').click()

            # Refresh Window and frame
            time.sleep(3)
            window = driver.window_handles[0]
            driver.switch_to.window(window)
            frame = driver.find_element_by_xpath('//frame[@name="content"]')
            driver.switch_to.frame(frame)

            # Check all classification matches
            checkboxes = []
            i = 0
            checkboxes = driver.find_elements_by_xpath("//input[@type='checkbox']")

            '''Check how many classification matches exist, if <50, skip, else check all and continue'''

            # //*[@id="datatable2"]/tbody
            # /html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/table/tbody

            # //*[@id="ClassificationsSearchGrid_ItemsGrid_ctl01_lblNumberOfReviewers"]
            # //*[@id="ClassificationsSearchGrid_ItemsGrid_ctl02_lblNumberOfReviewers"]
            # ...
            """
            allClassifications = driver.find_element_by_id("datatable2")
            reviewerCounter = 0
            for x in checkboxes-1:

                reviewerCounter += int(b)
                if x < 10:
                    b = string(driver.find_element_by_id(
                        "ClassificationsSearchGrid_ItemsGrid_ctl0" + x + "_lblNumberOfReviewers"))  # fix for string concatination
                    print(reviewerCounter)
                elif x >= 10:
                    b = string(driver.find_element_by_id(
                        "ClassificationsSearchGrid_ItemsGrid_ctl" + x + "_lblNumberOfReviewers"))  # fix for string concatination
                    print(reviewerCounter)

            # print("There are ", len(checkboxes), " total classification matches, selecting all.")

            c = input("Input any key to continue: ")  # Temporary manual breakpoint"""

            for check in checkboxes[1:]:
                check.click()
                i += 1
                # print("Check number: ", i)

            # Submit
            # print("Submitting...")

            # c = input("Input any key to continue: ")  # Temporary manual breakpoint

            driver.find_element_by_id(
                "ClassificationsSearchGrid_SubmitByClassificationsButton").click()

            # Refresh Window and frame
            time.sleep(3)
            window = driver.window_handles[0]
            driver.switch_to.window(window)
            frame = driver.find_element_by_xpath('//frame[@name="content"]')
            driver.switch_to.frame(frame)

            # Select random page that is not last Page
            # print("Selecting Random Page (Not last page)...")

            # c = input("Input any key to continue: ")  # Temporary manual breakpoint

            pages = []
            pages = driver.find_elements_by_class_name("paginationLink")

            reviewersAssigned = []
            count = 0

            if len(pages) < 3:  # only one or two pages: dont click any page value
                # print("There are less than 3 pages, staying with first page.")

                # print("Checking two board members, then 28 non board members...")
                x = 0
                pickTwoBoardMembers()
                # c = input("Temporary break: ")
                pickNonBoardMembers()

            else:
                print("length of pages = ", len(pages))
                rand = random.randrange(0, len(pages))  # select any except for last
                print("rand = ", rand)
                """
                try:
                    length = len(pages)-2  # -2 to account for the two arrows
                except:  # in case page numbers arent showing
                    length = 1
                # print("There are ", length, " pages on this selection.")
                if length > 10:
                    # print("There are more than 10 pages, setting max to 10...")
                    length = 10

                if length < 3:
                    rand = 1
                else:
                    rand = random.randrange(0, length-1)  # select any except for last"""
                # print("Random page choice: ", rand + 1)

                # if page == 1... continue like normal

                # if page !=1... click two from first page, then continue with count +=2

                if rand > 1:  # if page choice is not the first page, pick two then continue
                    # print("Checking two board members from first page, then 28 from the other page...")
                    x = 0
                    pickTwoBoardMembers()
                    # c = input("Temporary break: ")
                    try:
                        pages[rand].click()
                    except:
                        print("Unable to click random page")
                    # c = input("Temporary break: ")
                    pickNonBoardMembers()
                else:
                    # print("Checking two board members, then 28 non board members...")
                    x = 0
                    pickTwoBoardMembers()
                    # c = input("Temporary break: ")
                    pickNonBoardMembers()

                # Refresh Window and frame
                time.sleep(3)
                window = driver.window_handles[0]
                driver.switch_to.window(window)
                frame = driver.find_element_by_xpath('//frame[@name="content"]')
                driver.switch_to.frame(frame)

            # check two board members from first page

            # check 30 eligibile reviewers

            x = 0

            # c = input("Input any key to continue: ")  # Temporary manual breakpoint

            try:
                # click Proceed
                # driver.find_element_by_id('btnSubmit').click()  # //*[@id="btnSubmit"]
                driver.find_element_by_id('ProceedButton').click()  # //*[@id="btnSubmit"]

                time.sleep(4)
                window = driver.window_handles[0]
                driver.switch_to.window(window)
                frame = driver.find_element_by_xpath('//frame[@name="content"]')
                driver.switch_to.frame(frame)

                # wait for confirmation/continue
                print("Iterations = ", iterations)
                # print("Make sure that all the selected reviewers are good. If any are bad, check the 'do not assign' checkbox for them.")
                cont = 'y'  # temporary to remove user input
                # cont = input("Would you like to continue and repeat? (y/n): ") #useful for double checking after each article if necessary
                if(cont == 'y'):
                    # click confirm and send

                    # print("You sent a y, clicking confirm and continuing now...")
                    time.sleep(4)
                    window = driver.window_handles[0]
                    driver.switch_to.window(window)
                    frame = driver.find_element_by_xpath('//frame[@name="content"]')
                    driver.switch_to.frame(frame)

                    try:
                        submit = driver.find_element_by_id("ClassificationsSearchGrid_SubmitByClassificationsButton").click()
                    except:
                        submit = driver.find_element_by_id("btnSubmit").click()

                    #submit = driver.find_element_by_id("btnSubmit").click()
                    # driver.find_element_by_id('//*[@id="btnSubmit"]').click()
# //*[@id="ClassificationsSearchGrid_SubmitByClassificationsButton"]
                    # wait long time for it to send the emails
                    time.sleep(9)

                    # go back to last page:
                    # print("Clicking 'Return to New Editor Assignments' button now...")

                    window = driver.window_handles[0]
                    driver.switch_to.window(window)
                    frame = driver.find_element_by_xpath('//frame[@name="content"]')
                    driver.switch_to.frame(frame)

                    driver.find_element_by_id("linkReturn").click()

                else:
                    # print("Not a (y), exiting code now...")

                    break

                total -= 1  # decrease
                iterations += 1  # increase the count
                print("New iterations after completing this article = ", iterations)

            except:  # error: not enough reviewers to complete this article

                skips += 1

                time.sleep(5)
                window = driver.window_handles[0]
                driver.switch_to.window(window)
                frame = driver.find_element_by_xpath('//frame[@name="content"]')
                driver.switch_to.frame(frame)

                # click back to new assignments Button
                driver.find_element_by_id("linkReturnToEditorFolder1").click()

                # print(skips)
                if(articleNum == "fr100"):
                    # print("This was the last article on the page, going back a page...")

                    # go back a page...
                    driver.find_element_by_xpath(
                        '//*[@id="FGSubmissions"]/div[3]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[2]/table/tbody/tr/td[2]/a').click()
                    time.sleep(7)
                    window = driver.window_handles[0]
                    driver.switch_to.window(window)
                    frame = driver.find_element_by_xpath('//frame[@name="content"]')
                    driver.switch_to.frame(frame)

                # c = input("break")
                # print("Continuing with new skips: ", skips)

        else:
            pages = skips % 100
            # go to the correct page:
            print("skips >=100... pages = ", pages)
            c = input("break, ")
            for i in pages:
                c = input("break")
                # click next page
        print("Finished! Either max iterations have been reached, or user exited...\n Final iterations = ", iterations)

elif option == 2:  # 0 reviews completed
    iterations = 0

    total = int(input("How many iterations would you like to do?   "))

    print("Iterations = ", iterations)
    skips = 0
    # waiting = input("Get to the 'invite reviewers' page of one you want then send a key here: ")

    # print("Clicking 0 review articles now...")
    driver.find_element_by_id(
        'ctl00_Folders_SubmissionsRequiringMoreReviewers_FolderLink').click()

    # Refresh Window and frame
    time.sleep(5)
    window = driver.window_handles[0]
    driver.switch_to.window(window)
    frame = driver.find_element_by_xpath('//frame[@name="content"]')
    driver.switch_to.frame(frame)

    # c = input("Input any key to continue: ")  # Temporary manual breakpoint

    # click the organize by editor decision Button (left up arrow)
    # alt = "Sort Up"
    # button = driver.find_element_by_id(
    #     "//table[@id='datatable']//tr[last()-"+'{x}'.format(x=skips)+"]")
    # # ActionChains(driver).move_to_element(button).click(button).perform()
    # //*[@id="nfr0"]
    # articleNum = str(button.get_attribute('id'))
    decision = driver.find_element_by_id("nfr0")

    # print("Clicking sort by editor decision button.")
    if ("Major Revision" in decision.text):
        driver.find_element_by_xpath(
            '//*[@id="FGSubmissions"]/div[3]/div[1]/div[2]/div[2]/div[1]/table/thead/tr/th[10]/div/div/div[1]/div[1]/a').click()
        time.sleep(6)
    elif ("Minor Revision" in decision.text):
        driver.find_element_by_xpath(
            '//*[@id="FGSubmissions"]/div[3]/div[1]/div[2]/div[2]/div[1]/table/thead/tr/th[10]/div/div/div[1]/div[1]/a').click()
        time.sleep(6)
    else:
        pass

    #

    # wait the time

    time.sleep(5)
    window = driver.window_handles[0]
    driver.switch_to.window(window)
    frame = driver.find_element_by_xpath('//frame[@name="content"]')
    driver.switch_to.frame(frame)

    # pick the next article to do:

    while (total != 0):
        # print("Skips = ", skips)
        # print("Iterations completed = ", iterations)
        # print("Total remaining = ", total)

        check = False
        while (check == False):  # loop from first page to last element
            # c = input("Manual breakpoint. Input any key to continue: ")

            # print("Checking next article.", )

            button = driver.find_element_by_id("nfr"+'{x}'.format(x=skips))

            articleNum = str(button.get_attribute('id'))

            # print(button.text)
            # c = input("waiting")

            # check major/minor Revision (ignore if either exist)

            if("Major Revision" in button.text):
                print("Editor Decision contains a 'Revision'. You must have completed all possible non-revisions. The total amount you completed is: ", iterations)
                c = input(
                    "This is a final exit breakpoint, exit the code here after writing down 'iterations'!")
            if("Minor Revision" in button.text):
                print("Editor Decision contains a 'Revision'. You must have completed all possible non-revisions. The total amount you completed is: ", iterations)
                c = input(
                    "This is a final exit breakpoint, exit the code here after writing down 'iterations'!")

            elif ("Accept as is" in button.text):
                # print("Editor Decision contains a 'Accept as is'. Increasing skips...")
                if(articleNum == "row100"):
                    # print("All articles on this page are skips, going forwards a page...")
                    # go up a page...
                    driver.find_element_by_xpath(
                        '//*[@id="tableContainer"]/form/div/div[1]/table/tbody/tr/td[2]/a[6]').click()
                    time.sleep(7)
                    window = driver.window_handles[0]
                    driver.switch_to.window(window)
                    frame = driver.find_element_by_xpath('//frame[@name="content"]')
                    driver.switch_to.frame(frame)
                    skips = 0
                skips += 1

            elif ("Declined" not in button.text):  # make sure declined exists (continue only if exists)
                # print("None declined. Increasing skips...")
                if(articleNum == "row100"):
                    # print("All articles on this page are skips, going forwards a page...")
                    # go up a page...
                    driver.find_element_by_xpath(
                        '//*[@id="tableContainer"]/form/div/div[1]/table/tbody/tr/td[2]/a[6]').click()
                    time.sleep(7)
                    window = driver.window_handles[0]
                    driver.switch_to.window(window)
                    frame = driver.find_element_by_xpath('//frame[@name="content"]')
                    driver.switch_to.frame(frame)
                    skips = 0
                skips += 1
            else:
                if ("Invited" in button.text):
                    # print("Someone is still invited. Increasing skips...")
                    if(articleNum == "row100"):
                        # print("All articles on this page are skips, going forwards a page...")
                        # go up a page...
                        driver.find_element_by_xpath(
                            '//*[@id="tableContainer"]/form/div/div[1]/table/tbody/tr/td[2]/a[6]').click()
                        time.sleep(6)
                        window = driver.window_handles[0]
                        driver.switch_to.window(window)
                        frame = driver.find_element_by_xpath('//frame[@name="content"]')
                        driver.switch_to.frame(frame)
                        skips = 0
                    skips += 1

                elif("Agreed" in button.text):
                    # print("Someone has Agreed to this article. Increasing skips...")
                    if(articleNum == "row100"):
                        # print("All articles on this page are skips, going forwards a page...")
                        # go up a page...
                        driver.find_element_by_xpath(
                            '//*[@id="tableContainer"]/form/div/div[1]/table/tbody/tr/td[2]/a[6]').click()
                        time.sleep(6)
                        window = driver.window_handles[0]
                        driver.switch_to.window(window)
                        frame = driver.find_element_by_xpath('//frame[@name="content"]')
                        driver.switch_to.frame(frame)
                        skips = 0
                    skips += 1
                elif("Partial Review Saved" in button.text):
                    # print("Partial Review Saved. Increasing skips...")
                    if(articleNum == "row100"):
                        # print("All articles on this page are skips, going forwards a page...")
                        # go up a page...
                        driver.find_element_by_xpath(
                            '//*[@id="tableContainer"]/form/div/div[1]/table/tbody/tr/td[2]/a[6]').click()
                        time.sleep(6)
                        window = driver.window_handles[0]
                        driver.switch_to.window(window)
                        frame = driver.find_element_by_xpath('//frame[@name="content"]')
                        driver.switch_to.frame(frame)
                        skips = 0
                    skips += 1
                elif("Late" in button.text):
                    # print("There has been a late review. Increasing skips...")
                    if(articleNum == "row100"):
                        # print("All articles on this page are skips, going forwards a page...")
                        # go up a page...
                        driver.find_element_by_xpath(
                            '//*[@id="tableContainer"]/form/div/div[1]/table/tbody/tr/td[2]/a[6]').click()
                        time.sleep(6)
                        window = driver.window_handles[0]
                        driver.switch_to.window(window)
                        frame = driver.find_element_by_xpath('//frame[@name="content"]')
                        driver.switch_to.frame(frame)
                        skips = 0
                    skips += 1

                else:

                    # print("Clicking invite reviewers button for: ", str(button.get_attribute('id')))
                    check = True

                    # c = input("Breakpoint")
                    inviteVal = driver.find_element_by_id('fg-al-'+'{x}'.format(x=skips))

                    inviteVal.find_element_by_link_text("Invite Reviewers").click()

            # check if agree/invited exists (ignore if exists)

            # assuming all criteria are passed:

        # Temporary manual breakpoint
        # c = input("Decreasing 'total'. Input any key to continue: ")
        # total -= 1

        # print("Searching by Classification Matches...")
        driver.find_element_by_xpath(
            "//select[@name='ReviewerSearchOptions$HomeJournalSearchModeDropDown']/option[text()='Search by Classification Matches']").click()

        driver.find_element_by_xpath(
            '/html/body/div[1]/form/div[4]/div[3]/fieldset/table/tbody/tr/td[5]/input').click()

        # Refresh Window and frame
        time.sleep(3)
        window = driver.window_handles[0]
        driver.switch_to.window(window)
        frame = driver.find_element_by_xpath('//frame[@name="content"]')
        driver.switch_to.frame(frame)

        # Check all classification matches
        checkboxes = []
        i = 0
        checkboxes = driver.find_elements_by_xpath("//input[@type='checkbox']")

        # print("There are ", len(checkboxes), " total classification matches, selecting all.")

        # c = input("Input any key to continue: ")  # Temporary manual breakpoint

        for check in checkboxes[1:]:
            check.click()
            i += 1
            # print("Check number: ", i)

        # Submit
        # print("Submitting...")

        # c = input("Input any key to continue: ")  # Temporary manual breakpoint

        driver.find_element_by_id(
            "ClassificationsSearchGrid_SubmitByClassificationsButton").click()  # //*[@id="ClassificationsSearchGrid_SubmitByClassificationsButton"]

        # Refresh Window and frame
        time.sleep(3)
        window = driver.window_handles[0]
        driver.switch_to.window(window)
        frame = driver.find_element_by_xpath('//frame[@name="content"]')
        driver.switch_to.frame(frame)

        # Select random page that is not last Page
        # print("Selecting Random Page (Not last page)...")

        # c = input("Input any key to continue: ")  # Temporary manual breakpoint

        pages = []
        # pages = driver.find_elements_by_xpath(
        #     "/html/body/form/div[5]/div[1]/div[3]/div[2]/div[1]/table/tbody/tr/td[2]/*")
        # # pages = driver.find_element_by_id("ReviewersGrid_TopPaginator_paginatorPanel")
        pages = driver.find_elements_by_class_name("paginationLink")
        #/html/body/form/div[5]/div[1]/div[3]/div[2]/div[1]/table/tbody/tr/td[2]/span[2]

            #//*[@id="ReviewersGrid_TopPaginator_paginatorPanel"]/table/tbody/tr/td[2]/span[2]
  # //*[@id="ReviewersGrid_TopPaginator_paginatorPanel"]/table/tbody/tr/td[2]/span[2]
        reviewersAssigned = []
        count = 0
        length = len(pages)/2
        print("length = ", length)
        # print(pages)
        # c = input("break")
        if length < 3:  # only one or two pages: dont click any page value
            print("length of pages = ", length)
            print("There are less than 3 pages, staying with first page.")
            # c = input("small page count")

            # print("Checking two board members, then 28 non board members...")
            x = 0
            pickTwoBoardMembers()
            # c = input("Temporary break: ")
            pick22NonBoardMembers()

        else:
            print("length of pages = ", length)
            rand = random.randrange(0, length)  # select any except for last
            print("rand = ", rand)

            """
            try:  # in case there arent any page numbers for some reason
                length = len(pages)  # -2 to account for the two arrows
            except:
                length = 1

            # print("There are ", length, " pages on this selection.")
            if length > 10:
                # print("There are more than 10 pages, setting max to 10...")
                length = 10

            if length < 3:
                rand = 1
            else:
                rand = random.randrange(0, length)  # select any except for last
                print("rand = ", rand)"""
            # print("Random page choice: ", rand + 1)

            # if page == 1... continue like normal

            # if page !=1... click two from first page, then continue with count +=2

            if rand > 1:  # if page choice is not the first page, pick two then continue
                # print("Checking two board members from first page, then 28 from the other page...")

                x = 0
                pickTwoBoardMembers()
                # c = input("Temporary break: ")
                print("selecting random page: ", rand)
                # c = input("break")
                try:
                    pages[rand].click()
                except:
                    print("Unable to click random page")
                # c = input("Temporary break: ")
                pick22NonBoardMembers()
            else:
                # print("Checking two board members, then 28 non board members...")
                x = 0
                pickTwoBoardMembers()
                # c = input("Temporary break: ")
                pick22NonBoardMembers()

            # Refresh Window and frame
            time.sleep(3)
            window = driver.window_handles[0]
            driver.switch_to.window(window)
            frame = driver.find_element_by_xpath('//frame[@name="content"]')
            driver.switch_to.frame(frame)

        # check two board members from first page

        # check 30 eligibile reviewers

        x = 0

        # c = input("Input any key to continue: ")  # Temporary manual breakpoint
        try:
            # click Proceed
            driver.find_element_by_name('ProceedButton').click()

            time.sleep(3)
            window = driver.window_handles[0]
            driver.switch_to.window(window)
            frame = driver.find_element_by_xpath('//frame[@name="content"]')
            driver.switch_to.frame(frame)

            # wait for confirmation/continue
            # print("Make sure that all the selected reviewers are good. If any are bad, check the 'do not assign' checkbox for them.")
            cont = 'y'  # temporary to remove user input
            # cont = input("Would you like to continue and repeat? (y/n): ")
            if(cont == 'y'):
                # click confirm and send

                # print("You sent a y, clicking confirm and continuing now...")
                time.sleep(3)
                window = driver.window_handles[0]
                driver.switch_to.window(window)
                frame = driver.find_element_by_xpath('//frame[@name="content"]')
                driver.switch_to.frame(frame)

                submit = driver.find_element_by_name("btnSubmit").click()
                # driver.find_element_by_id('//*[@id="btnSubmit"]').click()

                # wait long time for it to send the emails
                time.sleep(9)

                # go back to last page:
                # print("Clicking 'Return to New Editor Assignments' button now...")

                window = driver.window_handles[0]
                driver.switch_to.window(window)
                frame = driver.find_element_by_xpath('//frame[@name="content"]')
                driver.switch_to.frame(frame)

                driver.find_element_by_id("linkReturn").click()
                iterations += 1
                total -= 1
                print("Iterations completed = ", iterations)
                print("Total remaining = ", total)

            else:
                # print("Not a (y), exiting code now...")
                break

            # iterations -= 1  # decrease
        except:
            # print("Continue a different article...")

            # click the go back button and wait
            driver.find_element_by_id("linkReturnToEditorFolder1").click()
            time.sleep(3)
            window = driver.window_handles[0]
            driver.switch_to.window(window)
            frame = driver.find_element_by_xpath('//frame[@name="content"]')
            driver.switch_to.frame(frame)

            skips += 1

    print("Iterations completed = ", iterations)
    print("Total remaining = ", total)
