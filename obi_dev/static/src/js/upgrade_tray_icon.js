odoo.define('obi_dev.systray.UpgradeMenu', function (require) {

"use strict";
var core = require('web.core');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var QWeb = core.qweb;

var UpgradeSystrayWidget = Widget.extend({
    name: 'upgrade_menu',
    template:'obi_dev.systray.UpgradeMenu',
    events: {
        'show.bs.dropdown': '_onUpgradeMenuShow',
        'click .o_obi_dev_module': '_onModuleClicked',
    },
    start: function () {
        this._$upgradeMenuIcon = this.$('.o_obi_dev_upgrade_items');
        var self = this;
        this.upgradeData = this._rpc({
            model: 'ir.module.module',
            method: 'get_non_basic',
        }).then(function(modules) {
            self.modules = modules;
            // modules.forEach(function(module_){
            // });
        });
    },
    _onUpgradeMenuShow: function(){
        var self = this;
        this.upgradeData.then(function (){
            self._$upgradeMenuIcon.html(QWeb.render('obi_dev.systray.UpgradeMenuItems', {
                modules : self.modules
            }));
        });
    },
    _onModuleClicked: function(ev){
        ev.stopPropagation();
        var moduleId = $(ev.currentTarget).data('module_id');
        this._rpc({
            model: 'ir.module.module',
            method: 'button_immediate_upgrade',
            args: [[moduleId]],
            context: {obi_upgrade: 'true story'},
        });
    },
});

UpgradeSystrayWidget.prototype.sequence = 1;
SystrayMenu.Items.push(UpgradeSystrayWidget);

});