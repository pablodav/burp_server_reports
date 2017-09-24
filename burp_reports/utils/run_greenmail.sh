#!/bin/bash
# Run greenmail with defaults tests ports to be used in unit tests
# Test setup for SMTP(S)/IMAP(S)/POP3(S) and two user
# Starts GreenMail for SMTP (test port 3025),
# SMTPS (test port 3465),
# IMAP (test port 3143),
# IMAPS (test port 3993),
# POP3 (test port 3110)
# and POP3S (test port 3995)
# using localhost/127.0.0.1 : 
cd burp_reports/utils/
java -Dgreenmail.setup.test.all -Dgreenmail.users=test1:pwd1,test2:pwd2@example.com -jar greenmail-standalone-1.5.5.jar &
