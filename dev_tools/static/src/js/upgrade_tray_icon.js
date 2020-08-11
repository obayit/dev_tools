odoo.define('dev_tools.systray.UpgradeMenu', function (require) {

"use strict";
var core = require('web.core');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var QWeb = core.qweb;
var session = require('web.session');

var UpgradeSystrayWidget = Widget.extend({
    name: 'upgrade_menu',
    template:'dev_tools.systray.UpgradeMenu',
    events: {
        'show.bs.dropdown': '_onUpgradeMenuShow',
        'click .o_dev_tools_module': '_onModuleClicked',
    },
    start: function () {
        this._$upgradeMenuIcon = this.$('.o_dev_tools_upgrade_items');
        var self = this;
        if(session.user_has_group('base.group_no_one')){
            this.upgradeData = this._rpc({
                model: 'ir.module.module',
                method: 'get_non_basic',
            }).then(function(modules) {
                self.modules = modules;
            });
        }
    },
    _onUpgradeMenuShow: function(){
        var self = this;
        this.upgradeData.then(function (){
            self._$upgradeMenuIcon.html(QWeb.render('dev_tools.systray.UpgradeMenuItems', {
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