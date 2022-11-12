# BANK system


A personal project I created. This project is a complete billing system, using PostgreSQL and flask HTTP serveres . <br/>
The system credits the customer with the amount.<br/>
In the following 12 weeks, the system performs debits of amount/12 once a week.<br/>
A failed debit is moved to the end of the repayment plan (a week from the last payment).<br/>
<br/><br/>


the system architecture:


<img src="images/arch.png">


## Processor
the processor supports 2 functions:
* perform_transaction - This call returns a transaction_id (random number betweem 10000-99999)

<br/>

*  download_report - 
Downloads a daily report of transaction results. It contains info about transactions from the last 5 days.

<br/>

## Billing system
the Billing system supports 1 functions:
* perform_advance - This call using the Processor functions and credits the customer with the amount.<br/>
In the following 12 weeks, the system performs debits of amount/12 once a week.<br/>
(all the prints and the logs are in the billing_system console)
<br/>

## The DATABASES
I chosed postgresDB database because it is a table type, it is reliable and it is fast.
In addition, the interface is very convenient.
<br/>
<br/>

the system flow:

<img src="images/flow.png">     

<br/><br/>


Example of the program (all the prints and the logs are in the billing_system console):

<img src="images/example.png">


<br/>

## Technologies
Project is created with:
* python: 3.11.0
* PostgreSQL: 15.0
* pgAdmin 4: 6.15



## Setup

* To run the processor:

```console
python processor/processor.py
```

* To run the billing system:
```console
python billing/billing_system.py
```

* To call the perform_advance API:
```console
python main.py
```


