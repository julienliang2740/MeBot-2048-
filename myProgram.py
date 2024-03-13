from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time

linesize = 4

def getTable(driver): #returns list of lists (format, vertical columns, left to right)
    # Initialize a 4x4 grid with all zeros
    grid = [[0 for _ in range(4)] for _ in range(4)]
    
    # Find all tiles by their class name
    tiles = driver.find_elements(By.CLASS_NAME, "tile")
    #print(tiles)
    
    for tile in tiles:
        # Extract the value inside the tile
        value = int(tile.find_element(By.CLASS_NAME, "tile-inner").text)
        
        # Extract the position of the tile
        classes = tile.get_attribute("class").split()
        for c in classes:
            if "tile-position" in c:
                position = c.split("-")[-2:]
                row, col = int(position[0]) - 1, int(position[1]) - 1
                break
        grid[row][col] = max(grid[row][col], value)
    
    return grid

def clone_grid(grid):
    return [row[:] for row in grid]

def mergeSingleLine(numLine):
    nozeroes = []
    mergedline = []

    for num in numLine:
        if num != 0:
            nozeroes.append(num)
    #print(nozeroes)

    i = 0
    while i < len(nozeroes):
        if i < len(nozeroes) - 1 and nozeroes[i] == nozeroes[i + 1]:
            mergedline.append(nozeroes[i] * 2)
            i += 2 # skip next element since it alr got merged
        else:
            mergedline.append(nozeroes[i])
            i += 1
    
    while len(mergedline) < linesize:
        mergedline.append(0)

    #print(mergedline)
    #print("---")
    return mergedline

def maxMerge(ogGrid, newGrid):
    ogListing = []
    newListing = []
    for row in ogGrid:
        for num in row:
            ogListing.append(num)
    for row in newGrid:
        for num in row:
            newListing.append(num)
    ogListing.sort(reverse=True)
    newListing.sort(reverse=True)

    for i in range(0,len(ogListing)):
        if ogListing[i] < newListing[i]:
            return newListing[i] 
    return 0

def up(theGrid):
    newGrid = clone_grid(theGrid)
    for i in range(0,linesize):
        newGrid[i] = mergeSingleLine(theGrid[i])
    return newGrid
    
def down(theGrid):
    newGrid = clone_grid(theGrid)
    for i in range(0,linesize):
        newGrid[i] = mergeSingleLine(theGrid[i][::-1])[::-1]
    return newGrid

def left(theGrid):
    newGrid = clone_grid(theGrid)
    for i in range(0,linesize):
        aLine = []
        for j in range(0,linesize):
            aLine.append(theGrid[j][i])
        aLineMerged = mergeSingleLine(aLine)
        for j in range(0,linesize):
            newGrid[j][i] = aLineMerged[j]
    return newGrid


def right(theGrid):
    newGrid = clone_grid(theGrid)
    for i in range(0,linesize):
        aLine = []
        for j in range(0,linesize):
            aLine.append(theGrid[j][i])
        aLineMerged = mergeSingleLine(aLine[::-1])[::-1]
        for j in range(0,linesize):
            newGrid[j][i] = aLineMerged[j]
    return newGrid

# Algos return: {"up", "down", "left", "right", "joever"}    

# Priority: down, left, right, up
def AlgoOne(theGrid): 
    if theGrid != down(theGrid):
        return "down"
    elif theGrid != left(theGrid):
        return "left"
    elif theGrid != right(theGrid):
        return "right"
    elif theGrid != up(theGrid):
        return "up"
    else:
        return "joever"

#Priority: max merge, down, left, right, up
def AlgoTwo(theGrid):
    upGrid = up(theGrid)
    downGrid = down(theGrid)
    leftGrid = left(theGrid)
    rightGrid = right(theGrid)

    if theGrid == upGrid and theGrid == downGrid and theGrid == leftGrid and theGrid == rightGrid:
        return "joever"
    
    upGridMax = maxMerge(theGrid, upGrid)
    downGridMax = maxMerge(theGrid, downGrid)
    leftGridMax = maxMerge(theGrid, leftGrid)
    rightGridMax = maxMerge(theGrid, rightGrid)

    maxMergeNum = max([upGridMax,downGridMax,leftGridMax,rightGridMax])
    
    if maxMergeNum != 0:
        if downGridMax == maxMergeNum:
            return "down"
        elif leftGridMax == maxMergeNum:
            return "left"
        elif rightGridMax == maxMergeNum:
            return "right"
        elif upGridMax == maxMergeNum:
            return "up"
    else:
        if theGrid != down(theGrid):
            return "down"
        elif theGrid != left(theGrid):
            return "left"
        elif theGrid != right(theGrid):
            return "right"
        elif theGrid != up(theGrid):
            return "up"
    
####################################################################################################
####################################################################################################
####################################################################################################

if __name__ == "__main__":

    options = Options()
    options.add_experimental_option("detach", True)

    service = Service(executable_path='chromedriver.exe')

    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://play2048.co/")

    # Ensure the game area is focused, here assuming the body can be focused
    driver.find_element(By.TAG_NAME, 'body').click()

    theTable = getTable(driver)
    print(theTable)

    actions = ActionChains(driver)

    while True:
        theTable = getTable(driver)
        print("The table: ")
        print(theTable)
        command = AlgoTwo(theTable)
        print("THE COMMAND:")
        print(command)

        if command == "joever":
            print("--------------------gAME jOEVER--------------------")
            break
        elif command == "up":
            actions.send_keys(Keys.ARROW_UP).perform()
            time.sleep(1)
        elif command == "down":
            actions.send_keys(Keys.ARROW_DOWN).perform()
            time.sleep(1)
        elif command == "left":
            actions.send_keys(Keys.ARROW_LEFT).perform()
            time.sleep(1)
        elif command == "right":
            actions.send_keys(Keys.ARROW_RIGHT).perform()
            time.sleep(1)
    time.sleep(1)

    """
    while True:
        ogTable = getTable(driver)

        actions.send_keys(Keys.ARROW_UP).perform()
        time.sleep(1)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(1)
        actions.send_keys(Keys.ARROW_LEFT).perform()
        time.sleep(1)
        actions.send_keys(Keys.ARROW_RIGHT).perform()
        time.sleep(1)

        newTable = getTable(driver)
        print(newTable)

        if (ogTable == newTable):
            print("--------------------gAME jOEVER--------------------")
            break

        print("bruga")
    """


    # driver.quit()  # You can comment this out if using detach, but typically you'd leave this in to close other resources.
