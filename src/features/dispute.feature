Feature: Disputes livecycle

  Scenario: Hold available funds on dispute
     Given an account
      And the account have deposited 10.0
      When a dispute is created
      Then the account should have available funds of 0.0
      And the account should have total funds of 10.0

  Scenario: Resolve an open dispute
     Given an account
      And the account have deposited 10.0
      And a dispute is created
      When the dispute is resolved
      Then the account should have available funds of 10.0
      And the account should have total funds of 10.0

  Scenario: Resolve an unknown dispute id does nothing
     Given an account
      And the account have deposited 10.0
      When a dispute is resolved
      Then the account should have available funds of 10.0
      And the account should have total funds of 10.0

  Scenario: Resolve on transaction without dispute does nothing
     Given an account
      And the account have deposited 10.0
      When the dispute is resolved
      Then the account should have available funds of 10.0
      And the account should have total funds of 10.0

  Scenario: Chargeback funds on dispute
     Given an account
      And the account have deposited 10.0
      And a dispute is created
      When the chargeback is created
      Then the account should have available funds of 0.0
      And the account should have total funds of 0.0
      And the account should be locked

  Scenario: Chargeback an unknown dispute id does nothing
     Given an account
      And the account have deposited 10.0
      When a chargeback is created
      Then the account should have available funds of 10.0
      And the account should have total funds of 10.0
      And the account should not be locked

  Scenario: Chargeback on transaction without dispute does nothing
     Given an account
      And the account have deposited 10.0
      When the chargeback is created
      Then the account should have available funds of 10.0
      And the account should have total funds of 10.0
      And the account should not be locked
