odoo.define('dev_tools.systray.InstallMenu', function (require) {

"use strict";
var core = require('web.core');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var QWeb = core.qweb;
var session = require('web.session');

var InstallSystrayWidget = Widget.extend({
    name: 'install_menu',
    template:'dev_tools.systray.InstallMenu',
    events: {
        'show.bs.dropdown': '_onInstallMenuShow',
        'click .o_dev_tools_module_event': '_onModuleClicked',
    },
    start: function () {
        this._$installMenuIcon = this.$('.o_dev_tools_install_items');
        var self = this;
        session.user_has_group('base.group_system').then(function(has_system_group){
            if(!has_system_group){
                self.$el.find('.o_obi_install_systray').hide();
                return;
            }
            self.installData = self._rpc({
                model: 'ir.module.module',
                method: 'get_non_basic',
                args: [false],
            }).then(function(modules) {
                self.modules = modules;
            });
        });
    },
    _onInstallMenuShow: function(){
        var self = this;
        this.installData.then(function (){
            self._$installMenuIcon.html(QWeb.render('dev_tools.systray.InstallMenuItems', {
                modules : self.modules
            }));
        });
    },
    _onModuleClicked: function(ev){
        ev.stopPropagation();
        var moduleId = $(ev.currentTarget).data('module_id');
        this._rpc({
            model: 'ir.module.module',
            method: 'button_immediate_install',
            args: [[moduleId]],
        });
    },
});

InstallSystrayWidget.prototype.sequence = 1;
SystrayMenu.Items.push(InstallSystrayWidget);

});