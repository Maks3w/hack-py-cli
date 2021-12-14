Feature: Deposit and withdraw operations

  Scenario: Increase funds after deposit
     Given an account with available funds of 10.0
      When a deposit of 10.0 is made
      Then the available funds should be 20.0
      And the total funds should be 20.0

  Scenario: Withdraw money from account
     Given an account with available funds of 10.0
      When a withdraw of 10.0 is made
      Then the available funds should be 0.0
      And the total funds should be 0.0

  Scenario: Withdraw money from account without enough available funds
      Given an account with available funds of 10.0
      When a withdraw of 20.0 is made
      Then the available funds should be 10.0
      And the total funds should be 10.0
      And a message should be displayed saying "Insufficient available funds"
