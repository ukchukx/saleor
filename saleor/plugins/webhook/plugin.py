from typing import TYPE_CHECKING, Any, List, Optional

from saleor.plugins.manager import from_payment_app_id

from ...payment import TransactionKind
from ...payment.interface import GatewayResponse, PaymentMethodInfo
from ...webhook.event_types import WebhookEventType
from ...webhook.payloads import (
    generate_checkout_payload,
    generate_customer_payload,
    generate_fulfillment_payload,
    generate_invoice_payload,
    generate_order_payload,
    generate_page_payload,
    generate_payment_payload,
    generate_product_deleted_payload,
    generate_product_payload,
    generate_product_variant_payload,
)
from ..base_plugin import BasePlugin
from .tasks import trigger_webhook_sync, trigger_webhooks_for_event

if TYPE_CHECKING:
    from requests.models import Response as RequestsResponse

    from ...account.models import User
    from ...checkout.models import Checkout
    from ...invoice.models import Invoice
    from ...order.models import Fulfillment, Order
    from ...page.models import Page
    from ...payment.interface import PaymentData
    from ...product.models import Product, ProductVariant


class WebhookPlugin(BasePlugin):
    PLUGIN_ID = "mirumee.webhooks"
    PLUGIN_NAME = "Webhooks"
    DEFAULT_ACTIVE = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = True

    def order_created(self, order: "Order", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        order_data = generate_order_payload(order)
        trigger_webhooks_for_event.delay(WebhookEventType.ORDER_CREATED, order_data)

    def order_confirmed(self, order: "Order", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        order_data = generate_order_payload(order)
        trigger_webhooks_for_event.delay(WebhookEventType.ORDER_CONFIRMED, order_data)

    def order_fully_paid(self, order: "Order", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        order_data = generate_order_payload(order)
        trigger_webhooks_for_event.delay(WebhookEventType.ORDER_FULLY_PAID, order_data)

    def order_updated(self, order: "Order", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        order_data = generate_order_payload(order)
        trigger_webhooks_for_event.delay(WebhookEventType.ORDER_UPDATED, order_data)

    def invoice_request(
        self,
        order: "Order",
        invoice: "Invoice",
        number: Optional[str],
        previous_value: Any,
    ) -> Any:
        if not self.active:
            return previous_value
        invoice_data = generate_invoice_payload(invoice)
        trigger_webhooks_for_event.delay(
            WebhookEventType.INVOICE_REQUESTED, invoice_data
        )

    def invoice_delete(self, invoice: "Invoice", previous_value: Any):
        if not self.active:
            return previous_value
        invoice_data = generate_invoice_payload(invoice)
        trigger_webhooks_for_event.delay(WebhookEventType.INVOICE_DELETED, invoice_data)

    def invoice_sent(self, invoice: "Invoice", email: str, previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        invoice_data = generate_invoice_payload(invoice)
        trigger_webhooks_for_event.delay(WebhookEventType.INVOICE_SENT, invoice_data)

    def order_cancelled(self, order: "Order", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        order_data = generate_order_payload(order)
        trigger_webhooks_for_event.delay(WebhookEventType.ORDER_CANCELLED, order_data)

    def order_fulfilled(self, order: "Order", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        order_data = generate_order_payload(order)
        trigger_webhooks_for_event.delay(WebhookEventType.ORDER_FULFILLED, order_data)

    def fulfillment_created(self, fulfillment: "Fulfillment", previous_value):
        if not self.active:
            return previous_value
        fulfillment_data = generate_fulfillment_payload(fulfillment)
        trigger_webhooks_for_event.delay(
            WebhookEventType.FULFILLMENT_CREATED, fulfillment_data
        )

    def customer_created(self, customer: "User", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        customer_data = generate_customer_payload(customer)
        trigger_webhooks_for_event.delay(
            WebhookEventType.CUSTOMER_CREATED, customer_data
        )

    def customer_updated(self, customer: "User", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        customer_data = generate_customer_payload(customer)
        trigger_webhooks_for_event.delay(
            WebhookEventType.CUSTOMER_UPDATED, customer_data
        )

    def product_created(self, product: "Product", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        product_data = generate_product_payload(product)
        trigger_webhooks_for_event.delay(WebhookEventType.PRODUCT_CREATED, product_data)

    def product_updated(self, product: "Product", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        product_data = generate_product_payload(product)
        trigger_webhooks_for_event.delay(WebhookEventType.PRODUCT_UPDATED, product_data)

    def product_deleted(
        self, product: "Product", variants: List[int], previous_value: Any
    ) -> Any:
        if not self.active:
            return previous_value
        product_data = generate_product_deleted_payload(product, variants)
        trigger_webhooks_for_event.delay(WebhookEventType.PRODUCT_DELETED, product_data)

    def product_variant_created(
        self, product_variant: "ProductVariant", previous_value: Any
    ) -> Any:
        if not self.active:
            return previous_value
        product_variant_data = generate_product_variant_payload(product_variant)
        trigger_webhooks_for_event.delay(
            WebhookEventType.PRODUCT_VARIANT_CREATED, product_variant_data
        )

    def product_variant_updated(
        self, product_variant: "ProductVariant", previous_value: Any
    ) -> Any:
        if not self.active:
            return previous_value
        product_variant_data = generate_product_variant_payload(product_variant)
        trigger_webhooks_for_event.delay(
            WebhookEventType.PRODUCT_VARIANT_UPDATED, product_variant_data
        )

    def product_variant_deleted(
        self, product_variant: "ProductVariant", previous_value: Any
    ) -> Any:
        if not self.active:
            return previous_value
        product_variant_data = generate_product_variant_payload(product_variant)
        trigger_webhooks_for_event.delay(
            WebhookEventType.PRODUCT_VARIANT_DELETED, product_variant_data
        )

    def checkout_created(self, checkout: "Checkout", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        checkout_data = generate_checkout_payload(checkout)
        trigger_webhooks_for_event.delay(
            WebhookEventType.CHECKOUT_CREATED, checkout_data
        )

    def checkout_updated(self, checkout: "Checkout", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        checkout_data = generate_checkout_payload(checkout)
        trigger_webhooks_for_event.delay(
            WebhookEventType.CHECKOUT_UPADTED, checkout_data
        )

    def page_created(self, page: "Page", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        page_data = generate_page_payload(page)
        trigger_webhooks_for_event.delay(WebhookEventType.PAGE_CREATED, page_data)

    def page_updated(self, page: "Page", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        page_data = generate_page_payload(page)
        trigger_webhooks_for_event.delay(WebhookEventType.PAGE_UPDATED, page_data)

    def page_deleted(self, page: "Page", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        page_data = generate_page_payload(page)
        trigger_webhooks_for_event.delay(WebhookEventType.PAGE_DELETED, page_data)

    def process_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        if not self.active:
            return previous_value

        # TODO: get App here somehow
        # HACK start
        from ...app.models import App
        from ...payment.models import Payment

        payment = Payment.objects.get(pk=payment_information.payment_id)
        app_id = from_payment_app_id(payment.gateway)
        app = App.objects.get(pk=app_id)
        webhook = app.webhooks.filter(
            is_active=True, events__event_type=WebhookEventType.PAYMENT_PROCESS
        )[0]
        print(webhook.__dict__)
        # HACK end

        webhook_payload = generate_payment_payload(payment_information)
        response = trigger_webhook_sync(
            webhook, WebhookEventType.PAYMENT_PROCESS, webhook_payload
        )

        def webhook_response_to_gateway_response(
            response: "RequestsResponse",
        ) -> "GatewayResponse":
            response_json = response.json()

            error = response_json.get("error")
            is_success = response.status_code == 200 and not error

            payment_method_info = PaymentMethodInfo(
                brand=response_json.get("payment_method_brand"),
                exp_month=response_json.get("payment_method_exp_month"),
                exp_year=response_json.get("payment_method_exp_year"),
                last_4=response_json.get("payment_method_last_4"),
                name=response_json.get("payment_method_name"),
                type=response_json.get("payment_method_type"),
            )

            return GatewayResponse(
                action_required=response_json.get("action_required", False),
                action_required_data=response_json.get("action_required_data"),
                amount=payment_information.amount,
                currency=payment_information.currency,
                customer_id=response_json.get("customer_id"),
                error=error,
                is_success=is_success,
                kind=TransactionKind.CAPTURE,
                transaction_id=response_json.get("transaction_id"),
                payment_method_info=payment_method_info,
                raw_response=response_json,
            )

        gateway_response = webhook_response_to_gateway_response(response)
        print("RESPONSE: ", gateway_response)
        # FIXME: check if this gets saved to the database
        return gateway_response
