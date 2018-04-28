Feature: The shopcart service back-end
    As an e-commerce customer
    I need a RESTful shopcart service
    So that I can keep track of all items in my shopcart

Background:
    Given the following items
        | sku    | name      | brand_name | price | count | is_available | link          |
        |  ID111 | Rlx341     | Rolex     | 1000  | 1     | True         | www.rolex.com |
        |  ID222 | AirMax     | Nike      | 150   | 2     | True         | www.nike.com  |
        |  ID333 | D5100      | Nikon     | 450   | 1     | True         | www.nikon.com |

Scenario: The server is running
    When I visit the "Cart page"
    Then I should see "SHOPCART REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create an Item
    When I visit the "Cart Page"
    And I set the "Name" to "Iphone"
    And I set the "Brand_name" to "Apple"
    And I set the "Sku" to "ID444"
    And I set the "Price" to "888.99"
    And I set the "Count" to "100"
    And I set the "Link" to "www.apple.com"
    And I press the "Create" button
    Then I should see the message "Success"

Scenario: List all items
    When I visit the "Cart Page"
    And I press the "Search" button
    Then I should see "Rlx341" in the results
    And I should see "AirMax" in the results
    And I should see "D5100" in the results

Scenario: Search by brand_name
    When I visit the "Cart Page"
    And I set the "Brand_name" to "Nike"
    And I press the "Search" button
    Then I should see "AirMax" in the results
    And I should not see "Rlx341" in the results
    And I should not see "D5100" in the results

Scenario: Update an Item
    When I visit the "Cart Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "Rlx341" in the "Name" field
    When I change "Name" to "Rolex45"
    And I press the "Update" button
    Then I should see the message "Success"
    When I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "Rolex45" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "Rolex45" in the results

Scenario: Delete an Item
    When I visit the "Cart Page"
    And I set the "Id" to "2"
    And I press the "Delete" button
    Then I should see the message "Item has been Deleted!"
    When I press the "Clear" button
    And I set the "Id" to "2"
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found: Item with id '2' was not found."

Scenario: Cancel all items
    When I visit the "Cart Page"
    And I press the "Search" button
    Then I should see "Rlx341" in the results
    And I should see "AirMax" in the results
    And I should see "D5100" in the results
    When I press the "Cancel" button
    Then I should not see "Rlx341" in the results
    And I should not see "AirMax" in the results
    And I should not see "D5100" in the results

