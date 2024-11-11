*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BOOK_NAME}     The Great Gatsby
${BOOK_AUTHOR}   F. Scott Fitzgerald

*** Test Cases ***

Validate HTTP GET /
    Create Session    mysession    http://127.0.0.1:8000
    ${response}=    GET On Session    mysession    /
    Should Be Equal As Strings    ${response.status_code}    200
    Should Be Equal As Strings    ${response.json()}[message]    hello world


Validate HTTP POST

    ${book}=    Create Dictionary    name=${BOOK_NAME}    author=${BOOK_AUTHOR}
    ${response}=    POST On Session    mysession    /books/add    json=${book}    expected_status=200
    Should Be Equal As Strings    ${response.status_code}    200
    Should Be Equal As Strings    ${response.json()}[message]    Book added successfully
#    close session
    Delete All Sessions