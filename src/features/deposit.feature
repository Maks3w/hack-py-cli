Feature: Deposit and withdraw operations

  Scenario: Increase funds after deposit
     Given an account
      And the account have deposited 10.0
      When a deposit of 10.0 is made
      Then the account should have available funds of 20.0
      And the account should have held funds of 0.0
      And the account should have total funds of 20.0

  Scenario: Withdraw money from account
     Given an account
      And the account have deposited 10.0
      When a withdraw of 10.0 is made
      Then the account should have available funds of 0.0
      And the account should have held funds of 0.0
      And the account should have total funds of 0.0

  Scenario: Withdraw money from account without enough available funds
     Given an account
      And the account have deposited 10.0
      When a withdraw of 20.0 is made
      Then the account should have available funds of 10.0
      And the account should have held funds of 0.0
      And the account should have total funds of 10.0
      And a message should be displayed saying "Insufficient available funds"
