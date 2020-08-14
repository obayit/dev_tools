odoo.define('dev_tools.systray.LogMenu', function (require) {

"use strict";
var core = require('web.core');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var QWeb = core.qweb;
var Bus = require('bus.Longpolling');
var session = require('web.session');
// var Bus = require('bus.BusService');

var LogSystrayWidget = Widget.extend({
    name: 'log_menu',
    template:'dev_tools.systray.LogMenu',
    dataLoad: 'Init data load',
    logLines: [],
    events: {
        'mouseover .o_obi_log_systray': '_onLogMenuShow',
        'click .dropdown-menu': '_onClick',
    },
    // bus: new Bus(),
    _onClick: function(isCalledNotClicked=false){
        if(! isCalledNotClicked){
            console.log('clicked');
        }
        this.upgradeData = this._rpc({
            model: 'odev.log',
            method: 'start',
        });
    },
    start: function () {
        core.bus.on('server_log_update', this, this._onLogUpdate);
        //TODO: read uid, and dbname from variables
        var uid = 2;
        var dbname = 'rsf12';
        // var channel = JSON.stringify([dbname, 'odev.log', session.uid]);
        var channel = "channel4"
        this.call('bus_service', 'addChannel', channel);
        // this.call('bus_service', 'onNotification', this, this.on_notification);
        this.call('bus_service', 'on', 'notification', this, this.on_notification);
        this.call('bus_service', 'startPolling');
        // this.bus.addChannel(channel);
        // this.bus.on("notification", this, this.on_notification);
        this._onClick(true);
        // this.bus.startPolling();
    },
    on_notification: function (notifications) {
        var self = this;
        _.each(notifications, function (notification) {
            var channel = notification[0];
            var message = notification[1];
            if (
                channel === 'channel4'
            ) {
                self.on_notification_do(message);
            }
        });
    },
    on_notification_do: function (message) {
        message = JSON.parse(message)
        var level = message[3];
        var wrezg_msg = message[4];
        var file = message[5];
        var message_class = '';
        switch (level) {
            case 'INFO':
                message_class = 'text-primary'
                break;
            case 'ERROR':
                message_class = 'text-danger'
                break;
            case 'WARNING':
                message_class = 'text-warning'
                break;
        
            default:
                message_class = 'text-primary'
                break;
        }
        this.logLines.push(message);
        this.$('.o_odev_log').append('<div><span class="' + message_class + '">' + level + '</span><span>'+
        wrezg_msg + '</span>' + '</div>');
    },
    _onLogUpdate: function(payload){
        if(typeof(payload) === typeof('')){
            this.dataLoad += payload;
        }
    },
    _onLogMenuShow: function(){
        
    },
});

LogSystrayWidget.prototype.sequence = 10;
// SystrayMenu.Items.push(LogSystrayWidget);
});