# Colatz

## Usage

from evolutionary import GASearch

search = GASearch()
search.search(1000)

## About

Use genetic algorithm to search for good candidate inputs to the algorithm at the heart of the Colatz Conjecture.  Good candidates in this case means ones that yield long sequences of increasing values.

Solutions (candidate inputs) are positive integers encoded as binary sequences.
