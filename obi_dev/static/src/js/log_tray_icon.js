odoo.define('obi_dev.systray.LogMenu', function (require) {

"use strict";
var core = require('web.core');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var QWeb = core.qweb;

var LogSystrayWidget = Widget.extend({
    name: 'log_menu',
    template:'obi_dev.systray.LogMenu',
    dataLoad: '',
    events: {
        'mouseover .o_obi_log_systray': '_onLogMenuShow',
    },
    start: function () {
        this._$upgradeMenuIcon = this.$('.o_obi_dev_upgrade_items');
        var self = this;
        core.bus.on('server_log_update', this, this._onLogUpdate);
        this.upgradeData = this._rpc({
            model: 'ir.module.module',
            method: 'get_non_basic',
        }).then(function(modules) {
            self.modules = modules;
            // modules.forEach(function(module_){
            // });
        });
    },
    _onLogUpdate: function(payload){
        this.dataLoad += payload;
    },
    _onLogMenuShow: function(){
        var self = this;
        this.upgradeData.then(function (){
            self._$upgradeMenuIcon.html(QWeb.render('obi_dev.systray.LogMenuItems', {
                modules : self.modules
            }));
        });
    },
});

LogSystrayWidget.prototype.sequence = 10;
SystrayMenu.Items.push(LogSystrayWidget);
});