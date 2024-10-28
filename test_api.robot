*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}    http://127.0.0.1:8000

*** Test Cases ***
Test Root Endpoint

    Create Session    api    ${BASE_URL}
    ${response}=    GET On Session    api    /
    Status Should Be    200    ${response}
    Dictionary Should Contain Item    ${response.json()}    Hello    test123