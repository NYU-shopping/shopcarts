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
