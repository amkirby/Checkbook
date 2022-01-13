
# yaml config
in theory, easier "user customization" than using python files
## print constants
### values that can be in yaml
* - [ ] DATE_SIZE
* - [ ] TRANS_SIZE
* - [ ] DESC_SIZE
* - [ ] AMOUNT_SIZE
* - [ ] NUM_SIZE
* - [ ] CAT_SIZE
* - [ ] HLINE_CHAR
* - [ ] VLINE_CHAR

### other discussion
the SIZE_LIST can be set in the configuration class

## config
### values that can be in yaml
* - [ ] DATE_FORMAT
* - [ ] THOUSAND_SEP
* - [ ] USE_SQL
* - [ ] FILE_NAME
* - [ ] DB_NAME
* - [ ] Category Values -> how to do lists in yaml (future project to nest categories)
  * Debit
  * Credit
* - [ ] SORT_BY_KEY

### other discussion
should locale be in yaml?

DEBIT_MULTIPLIER? still needed?

CATEGORIES & CATEGORIES_TO_ADD will be set in the configuration class

## commands
nothing should be in the yaml