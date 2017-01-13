openerp.pos_email_receipt = function(instance){
	var module = instance.point_of_sale;
    var _t     = instance.web._t;
    var QWeb   = instance.web.qweb;
    var no = 1
    
    module.ReceiptScreenWidget = module.ScreenWidget.extend({
        template: 'ReceiptScreenWidget',

        show_numpad:     false,
        show_leftpane:   false,

        show: function(){
            this._super();
            var self = this;

            var print_button = this.add_action_button({
                    label: _t('Print'),
                    icon: '/point_of_sale/static/src/img/icons/png48/printer.png',
                    click: function(){ self.print(); },
                });

            var finish_button = this.add_action_button({
                    label: _t('Next Order'),
                    icon: '/point_of_sale/static/src/img/icons/png48/go-next.png',
                    click: function() { self.finishOrder(); },
                });

            var email_button = this.add_action_button({
                    label: _t('Send Email'),
                    icon: '/pos_email_receipt/static/src/img/icons/email.png',
                    click: function() { self.sendMail(); },
                });

            this.refresh();

            if (!this.pos.get('selectedOrder')._printed) {
                this.print();
            }

            //
            // The problem is that in chrome the print() is asynchronous and doesn't
            // execute until all rpc are finished. So it conflicts with the rpc used
            // to send the orders to the backend, and the user is able to go to the next 
            // screen before the printing dialog is opened. The problem is that what's 
            // printed is whatever is in the page when the dialog is opened and not when it's called,
            // and so you end up printing the product list instead of the receipt... 
            //
            // Fixing this would need a re-architecturing
            // of the code to postpone sending of orders after printing.
            //
            // But since the print dialog also blocks the other asynchronous calls, the
            // button enabling in the setTimeout() is blocked until the printing dialog is 
            // closed. But the timeout has to be big enough or else it doesn't work
            // 2 seconds is the same as the default timeout for sending orders and so the dialog
            // should have appeared before the timeout... so yeah that's not ultra reliable. 

            finish_button.set_disabled(true);   
            setTimeout(function(){
                finish_button.set_disabled(false);
            }, 2000);
        },
        print: function() {
            this.pos.get('selectedOrder')._printed = true;
            window.print();
        },
        sendMail: function(){
        	var self = this;
        	var pos_ref = this.pos.get('selectedOrder').get('name');
        	var mail = prompt("Please enter your Email", "example@example.com");
        	var name = mail.split("@");
        	while (name.length!=2){
	        	var mail = prompt("Please enter valid Email", "example@example.com");
	        	var name = mail.split("@");
        	}
        	url=window.location.href;


			openerp.session.rpc('/web/dataset/resequence', {
				model: 'pos.order',
				ids: [],
				offset: 42
			}).then(function (result) {
				new instance.web.Model('pos.order').call('send_mail_customer',[pos_ref, mail]);
				// resequence didn't error out
			}, function () {
				alert("Server is not working....!!")
				// an error occured during during call
			});

        },
        finishOrder: function() {
            this.pos.get('selectedOrder').destroy();
        },
        refresh: function() {
            var order = this.pos.get('selectedOrder');
            $('.pos-receipt-container', this.$el).html(QWeb.render('PosTicket',{
                    widget:this,
                    order: order,
                    orderlines: order.get('orderLines').models,
                    paymentlines: order.get('paymentLines').models,
                }));
        },
        close: function(){
            this._super();
        }
    });

}
