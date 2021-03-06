//// -- LEVEL 1
//// -- Tables and References

// Creating tables
Table INVOICES as I {
	sk_invoice int8 [pk, increment] 
	id_invoice varchar(50)
	fk_agency_id int8
	fk_client_id int8
	fk_created_by_id int8
	fk_payer_id int8
	fk_rectify_invoice_id int8
	tm_created_at timestamp(6)
	dt_date date(0)
	cd_code varchar(50)
	cd_currency varchar(5)
	ds_cd_country varchar(5)
	ds_billing_period varchar(30)
	ds_cd_payment_terms varchar(100)
}

Table SALES as S {
	sk_sale int8 [pk, increment]
	id_sale varchar(50)
	fk_agency_id int8
	fk_user_id int8
	fk_created_by_id int8
	fk_invoice_id int8 [ref: > I.sk_invoice]
	fk_client_id int8
	fk_rectify_sale_id int8
	dt_date date(0)
	tm_created_at timestamp(6)
	qt_amount float8
	cd_is_country varchar(5)
	cd_code varchar(50)
	cd_currency varchar(5)
	ds_payment_method varchar(25)
	ds_cd_billing_period varchar(30)
	ds_cd_payment_term varchar(100)
	in_invoiceable boolean
	in_skip_receipt boolean
	in_cd_skip_invoicing boolean
}

Table INVOICE_ENTRIES as IE {
	fk_invoice int(8)  [ref: > I.sk_invoice]
	cd_code varchar(50)
	ds_description varchar(1000)
	qt_price float8
	qt_quantity float8
	ds_region_slug varchar(30)
	fk_sale_id int8 [ref: - S.sk_sale]
	ds_tax_code varchar(30)
	qt_discount float8
	ad_inserted_at timestamp(6)
}

Table PAYMENT as P {
	sk_payment int8
	id_payment varchar(50)
	fk_agency_id int8
	fk_client_id int8
	fk_created_by_id int8
	fk_invoice_id int8  [ref: - I.sk_invoice]
	fk_journey_id int8
	fk_payment_method_id int8
	fk_sale_id int8 [ref: - S.sk_sale]
	fk_user_id int8
	tm_created_at timestamp(6)
	dt_due_date date(0) 
	ds_state varchar(50)
	ds_intent varchar(50)
	ds_gateway_slug varchar(50)
	qt_ev_amount float8 
}

Table PAYMENT_TRANSACTION as PT {
	sk_paymenttransaction int8
	fk_payment_id int8 [ref: > P.sk_payment]
	fk_opt_journey_id int8
	fk_payment_method_id int8
	fk_opt_embedded_journey_id int8
	fk_opt_embedded_payment_method_id int8
	fk_opt_reference_transaction_id int8
	fk_user_id int8
	ds_type varchar(50)
	ds_action varchar(30)
	ds_requested varchar(50)
	cd_amount_currency varchar(5)
	cd_gateway_slug varchar(50)
	in_opt_success boolean
	qt_debt_settled_value float8
}


Table SALES_ENTRIES as SE {
	fk_sale int8 [ref: > S.sk_sale]
	cd_code varchar(50)
	cd_currency varchar(5)
	ds_description varchar(5000)
	dt_date date(0)
	qt_discount float(8)
	fk_journey_id int8 [ref: > J.sk_journey]
	qt_price float8
	qt_quantity float8
	ds_region_slug varchar(30)
	ds_tax_code varcahr(30)
	qt_discount_local float8
	qt_discount_usd float8
	qt_price_local float8
	qt_price_usd float8
	ad_inserted_at timestamp(6)
}

Table JOURNEY as J {
  sk_journey int8 [pk, increment]
  id_journey varchar (50)
  fk_agency_id int8
  fk_client_id int8
  fk_company_id int8
  fk_payer_id int8
  fk_product_id int8
  fk_preferred_driver_id int8
  fk_region_id int8
  fk_rider_id int8
  fk_user_id int8
  fk_taxi_id int8
  fk_driver_shift int8
  fk_end_state_id int8
  fk_start_type_id int8
  fk_start_zone_id int8
  fk_vehicle_type_id int8
  fk_driver_id int8
  fk_group_id int8
  fk_pricing_group_id int8
  fk_loyalty_program_id int8
  ds_amount_paid varchar(255)
  ds_amount_payable varchar(255)
  tm_arrived_utc_at timestamp(6)
  dt_arrived_utc_at date(0)
  tm_arrived_local_at timestamp(6)
  dt_arrived_local_at date(0)
  cd_currency varchar(5)
  qt_cost float8
  qt_discount float8
  qt_distance float8
  qt_duration float8
  qt_price float8
  in_authorisation_requested boolean
}

Table COMPANY_INVOICE as CI {
 sk_companyinvoice int8 [pk, increment]
 id_companyinvoice varchar(50)
 fk_agency_id int8
 cd_code varchar(50)
 fk_company_id int8
 tm_created_at timestamp(6)
 cd_currency varchar(5)
 dt_date date(0)
 ds_kind varchar(50)
 ds_series varchar(50)
 ds_state varchar(50)
 ds_type varchar(50)
 tm_updated_at timestamp(6)
 in_delete boolean
 dt_value_date date(0)
 ds_notes varchar(50)
 id_issuer_id varchar(50)
 ds_issuer_name varchar(50)
 id_invoicexpress_id varchar(50)
 ds_tax_region_state varchar(50)
 ad_inserted_at timestamp(6)
}

Table COMPANY_INVOICE_ENTRY as CIE {
 sk_companyinvoice_entry int8 [pk, increment]
 fk_companyinvoice int8 [ref: > CI.sk_companyinvoice]
 cd_code varchar(5)
 ds_description varchar(50)
 fk_driver_penalty_id int8 [ref: - DPY.sk_driverpenalty]
 fk_journey_id int8 [ref: - J.sk_journey]
 fk_driver_payout_id int8 [ref: - DP.sk_driverpayout]
 fk_driver_bonus_id int8 [ref: - DB.sk_driverbonus]
 qt_price float8
 qt_quantity float8
 ds_tax_code varchar(5)
 ds_description_encript varchar(50)
}

Table DRIVER_PAYOUT as DP {
 sk_driverpayout int8 [pk, increment] 
 id_driverpayout varchar(50)
 fk_agency_id int8
 cd_amount_currency varchar(50)
 qt_amount_value int8
 ds_category varchar(50)
 fk_company_id int8
 fk_created_by_id int8
 fk_driver_id int8
 qt_amount_value_local int8
 qt_amount_value_usd int8
 }
 
Table DRIVER_BONUS as DB {
 sk_driverbonus int8 [pk, increment]
 id_driverbonus varchar(50)
 fk_agency_id varchar(50)
 cd_amount_currency varchar(5)
 qt_amount_value int8
 ds_category varchar(50)
 fk_company_id int8
 fk_created_by_id int8
 fk_driver_id int8
 fk_region_id int8
}

Table DRIVER_PENALTY as DPY {
 sk_driverpenalty int8 [pk, increment]
 id_driverpenalty varchar(50)
 fk_agency_id varchar(50)
 cd_amount_currency varchar(5)
 qt_amount_value int8
 fk_company_id int8
 fk_created_by_id int8
 fk_driver_id int8
 fk_region_id int8
}