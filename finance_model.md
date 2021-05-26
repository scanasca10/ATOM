>>## Main Concepts 
>
>- *users* = each person that it is registered in the Cabify system.
>- *rider* = the user that enjoys the service.
>- *driver* = the user how drives the cab.
>- *company* = it refers to the user drivers, usually a company have at least one or several drivers.
>- *client* = the user who orders the service, there are three types of riders (Private, Corporate, Self Catering).
>- *agency* = country.
>
>>## ERD Finance Model 
>
>![Captura de pantalla 2020-04-30 a las 12.26.31](images/Captura_de_pantalla_2020-04-30_a_las_12.26.31.png)
>
>To find more info please here it is the [diagram](https://dbdiagram.io/d/5ea97ec339d18f5553fe6c13)
>
>
>>## Relationships 
>
>A payment (`fin_fac_payment`) can be done through a sale (`fin_dim_sale`) or through an invoice (`fin_dim_invoice`). 
>
>All invoice (`fin_dim_invoice`) has 1 or more sales (`fin_dim_sale`).
>
>Not all sale (`fin_dim_sale`) has an invoice (`fin_dim_invoice`)
>
>![Captura de pantalla 2020-04-30 a las 12.23.51](images/Captura_de_pantalla_2020-04-30_a_las_12.23.51.png)
>
>In order to see if the payment deadlines are met we have to compare `dt_date` (from `fin_dim_invoice`or `fin_dim_sale`)  with the field `dt_due_date` (`fin_fac_payment`).
>
>
>>## Client
>
>One client can have one or more users (**1:n**). 
>
>Here it is a client segmentation based on their way of working with Cabify:
>
>-  **Private** clients are *not_invoiceable* (payment through sale).
>
>- **Corporate** clients are *invoiceable* (payment through invoice).
>
>- Exceptions are **Self Catering** clients which are *private* clients but with *invoice*. Payment on receipt.
>
>
>
>> ## Sale Rectification
>
>> In case of need to edit a sale, it will generate a new sale: Let's see the next example:
>
>- sale = 4, rectify_sale_id = 5, journey = 1, price = 10, quantity = 1, discount = 0 (By error we did not include a discount of 4)
>- sale = 5, rectify_sale_id = -1, journey = 1, price = 10, quantity = -1, discount = 0
>- sale = 6, rectify_sale_id = -1, journey = 1, price = 10, quantity = 1, discount = 4
>
>The `fk_rectify_sale_id` in the table sale (`fin_dim_sale`) points out to the sale record that rectify the current sale. In the previous example, the sale 4 is rectified by the sale 5 (quantity = -1).
>
>Here it is a real example:
>
>![Captura de pantalla 2020-04-29 a las 12.41.09](images/Captura_de_pantalla_2020-04-29_a_las_12.41.09.png)
>
>> ## Payment 
>>
>> ### Status
>>
>> This is a photo of the final state of a payment, last state of the payment transaction
>
>- *pending*: this is the temporal state between other states. 
>
>- *declined*: The payment has been denied, payment not paid.
>
>- *chargeback*: The client asks to get his money back.
>
>- *authorised*: The payment amount is blocked at the chosen payment method.
>
>- *captured*: Cabify receives the money.
>
>- *cancelled*: The payment has been cancelled.
>
>- *requested*:  Corporate client with invoice, the money should be paid before the due_date.
>
>- *refunded*: The payment has been refund.
>
>  
>
>> ## Payment
>>
>> ### Lifecycle
>
>Every payment have two possible intents  `ds_intent` {authorised | purchase}. 
>
>First, every payment has an `ds_intent` = *authorised* , this state represents a block of the chargeable amount in the chosen payment method, expect for cash payments. 
>
>Finally, the payment has an `ds_intent` = *purchased* , this state represents valid chance for payment but it does not mean a successful payment.
>
>> Every sale or invoice have at least two payments, except in the case of cash payment  (only purchased)
>
>Every payment (`fin_fac_payment`)  contains several payment_ transactions (`fin_fac_paymenttransaction`)
>
>![Captura de pantalla 2020-04-30 a las 11.24.26](images/Captura_de_pantalla_2020-04-30_a_las_11.24.26.png)
>
>There are three important fields at the payment_transaction table  (`fin_fac_paymenttransaction`)  which are: `ds_requested`, `ds_action`, `in_opt_success` because they determine the payment state except for the state *requested*.
>
>> The payment state is a photo of the state of the last payment_transaction
>
>![Captura de pantalla 2020-04-29 a las 18.33.27](images/Captura_de_pantalla_2020-04-30_a_las_16.14.41.png)
>
>For the cases where the field `in_opt_sucess` = *false* it can be errors or it can be fraud, the amount of debt associated is (`qt_debt_settled_value`).
>
>
>> ## Did you know?
>
>- A sale (`fin_dim_sale`) will be considered finished **ONLY** when its status is closed `ds_sale_state` = 'closed'
>
>- Each invoice_entry (`fin_dim_invoice_entries`) gerenates a sale (`fin_dim_sale`)
>
>- The only way to relate a sale (`fin_dim_sale`) with a journey (`ops_fac_journey`) is through a sale_entry (`fin_dim_sale_entries`)
>
>- The *price* does not take into account the *discount*
>
>- All the fields related to amount (*qt_price*, *qt_discount*, *qt_cost*, *qt_distance*, *qt_duration*, *qt_debt_settled_value*...) without the `_local` clause do not have decimal part expect for **Colombia** and **Chile**. 
>
>  > This mean we have to divide by 100 those cases.
