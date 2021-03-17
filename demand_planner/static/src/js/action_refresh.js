odoo.define('demand_planner.action_refresh', function (require) {
	"use strict";
var core = require('web.core');
var ListController = require('web.ListController');
var rpc = require('web.rpc');
var session = require('web.session');
var _t = core._t;
ListController.include({
   renderButtons: function($node) {
   this._super.apply(this, arguments);
       if (this.$buttons) {
         this.$buttons.find('.oe_action_button').click(this.proxy('action_refresh')) ;
       }
   },
   action_refresh: function () {
            var self =this;
            var user = session.uid;
            rpc.query({
                model: 'demand.planner',
                method: 'get_data',
                context: session.user_context,
                args: [[user]],
                }).then(function (e) {
                  self.trigger_up('reload');
                });
            },
        });
});

  