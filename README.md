## Introduction

This repository contains the code written by Group 8 for the Information Systems Address Verification System (AVS) Capstone Project at Kennesaw State University. 

## Quick Start

## Technical Details

### Summary

Our implementation of the Address Verification System uses Quart, a Python web framework, interfacing with Redis for storing key-value pairs and SQLite for storing auth credentials. Our database abstraction layers are Redis-py (for Redis) and SQLAlchemy (for SQLite). Address verification is largely handled by RediSearch, which supports Levenshtein distance fuzzy matching. Inbound and outbound request data is cleaned and validated with Pydantic models. Without auth, API response times are less than 10 milliseconds. 

### Quick Start


### Some additional notes

* The Python code required to make this work vs. using `levenshtein` with Postgres is likely similar (if not slightly more for our approach), but using Redis and RediSearch provides additional speed and scalability, with the added caveat that Redis is both more difficult to configure and more temperamental as an in-memory data store. 
