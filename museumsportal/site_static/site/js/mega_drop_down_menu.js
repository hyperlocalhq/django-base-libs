/* global window:false, lscache:false */

$(window).load(function() {
    var MAPPER = {
        // de
        'menu-museen': 'mega_museums',
        'menu-ausstellungen': 'mega_exhibitions',
        'menu-veranstaltungen': 'mega_events',
        'menu-fuhrungen': 'mega_workshops',
        'menu-planen-organisieren': 'mega_plan_your_visit',
        // en
        'menu-museums': 'mega_museums',
        'menu-exhibitions': 'mega_exhibitions',
        'menu-events': 'mega_events',
        'menu-guided-tours': 'mega_workshops',
        'menu-plan-your-visit': 'mega_plan_your_visit',
        // pl
        'menu-muzea': 'mega_museums',
        'menu-wystawy': 'mega_exhibitions',
        'menu-wydarzenia': 'mega_events',
        'menu-oprowadzanie': 'mega_workshops',
        'menu-planowanie-organizacja': 'mega_plan_your_visit',
        // fr
        'menu-musees': 'mega_museums',
        'menu-expositions': 'mega_exhibitions',
        'menu-spectacles': 'mega_events',
        'menu-visites-guidees': 'mega_workshops',
        'menu-planifier-organiser': 'mega_plan_your_visit',
        // it
        'menu-musei': 'mega_museums',
        'menu-mostre': 'mega_exhibitions',
        'menu-manifestazioni-culturali': 'mega_events',
        'menu-visite-guidate': 'mega_workshops',
        'menu-organizza-la-tua-visita': 'mega_plan_your_visit',
        // tr
        'menu-muzeler': 'mega_museums',
        'menu-sergiler': 'mega_exhibitions',
        'menu-etkinlikler': 'mega_events',
        'menu-rehberli-turlar-ve-atolyeler': 'mega_workshops',
        'menu-planlamak-organize-etmek': 'mega_plan_your_visit'
    };

	var Datepicker = function(element, picker, options){
		this.element = $(element);
		this.format = DPGlobal.parseFormat(options.format||this.element.data('date-format')||'mm/dd/yyyy');
		this.picker = picker.on({
            click: $.proxy(this.click, this),
            mousedown: $.proxy(this.mousedown, this)
        });
		this.isInput = this.element.is('input');
		this.component = this.element.is('.date') ? this.element.find('.add-on') : false;

        this.callback = options.callback;

		if (this.isInput) {
		    /*
			this.element.on({
				focus: $.proxy(this.show, this)
			});
			*/
		} else {
			if (this.component){
				this.component.on('click', $.proxy(this.show, this));
			} else {
				this.element.on('click', $.proxy(this.show, this));
			}
		}
		this.minViewMode = options.minViewMode||this.element.data('date-minviewmode')||0;
		if (typeof this.minViewMode === 'string') {
			switch (this.minViewMode) {
				case 'months':
					this.minViewMode = 1;
					break;
				case 'years':
					this.minViewMode = 2;
					break;
				default:
					this.minViewMode = 0;
					break;
			}
		}
		this.viewMode = options.viewMode||this.element.data('date-viewmode')||0;
		if (typeof this.viewMode === 'string') {
			switch (this.viewMode) {
				case 'months':
					this.viewMode = 1;
					break;
				case 'years':
					this.viewMode = 2;
					break;
				default:
					this.viewMode = 0;
					break;
			}
		}
		this.startViewMode = this.viewMode;
		this.weekStart = options.weekStart||this.element.data('date-weekstart')||0;
		this.weekEnd = this.weekStart === 0 ? 6 : this.weekStart - 1;
		this.fillDow();
		this.fillMonths();
		this.update();
		this.showMode();
		this.set();
	};

	Datepicker.prototype = {
		constructor: Datepicker,

		show: function(e) {
			this.height = this.component ? this.component.outerHeight() : this.element.outerHeight();
			if (e ) {
				e.stopPropagation();
				e.preventDefault();
			}
			this.element.trigger({
				type: 'show',
				date: this.date
			});
		},

		set: function() {
			var formated = DPGlobal.formatDate(this.date, this.format);
			$('date', this.picker).text(formated);
			/*
			if (!this.isInput) {
				if (this.component){
					this.element.find('input').prop('value', formated);
				}
				this.element.data('date', formated);
			} else {
				this.element.prop('value', formated);
			}
			*/
		},

		setValue: function(newDate) {
			if (typeof newDate === 'string') {
				this.date = DPGlobal.parseDate(newDate, this.format);
			} else {
				this.date = new Date(newDate);
			}
			this.set();
			this.viewDate = new Date(this.date.getFullYear(), this.date.getMonth(), 1, 0, 0, 0, 0);
			this.fill();
		},

		update: function(newDate){
			this.date = DPGlobal.parseDate(
				typeof newDate === 'string' ? newDate : (this.isInput ? this.element.prop('value') : this.element.data('date')),
				this.format
			);
			this.viewDate = new Date(this.date.getFullYear(), this.date.getMonth(), 1, 0, 0, 0, 0);
			this.fill();
		},

		fillDow: function(){
			var dowCnt = this.weekStart;
			var html = '<tr>';
			while (dowCnt < this.weekStart + 7) {
				html += '<th class="dow">'+DPGlobal.dates.daysMin[(dowCnt++)%7]+'</th>';
			}
			html += '</tr>';
			this.picker.find('.datepicker-days thead').append(html);
		},

		fillMonths: function(){
			var html = '';
			var i = 0;
			while (i < 12) {
				html += '<span class="month">'+DPGlobal.dates.monthsShort[i++]+'</span>';
			}
			this.picker.find('.datepicker-months td').append(html);
		},

		fill: function() {
			var d = new Date(this.viewDate),
				year = d.getFullYear(),
				month = d.getMonth(),
				currentDate = this.date.valueOf();
			this.picker.find('.datepicker-days th:eq(1)')
						.text(DPGlobal.dates.months[month]+' '+year);
			var prevMonth = new Date(year, month-1, 28,0,0,0,0),
				day = DPGlobal.getDaysInMonth(prevMonth.getFullYear(), prevMonth.getMonth());
			prevMonth.setDate(day);
			prevMonth.setDate(day - (prevMonth.getDay() - this.weekStart + 7)%7);
			var nextMonth = new Date(prevMonth);
			nextMonth.setDate(nextMonth.getDate() + 42);
			nextMonth = nextMonth.valueOf();
			var html = [];
			var clsName;
			while(prevMonth.valueOf() < nextMonth) {
				if (prevMonth.getDay() === this.weekStart) {
					html.push('<tr>');
				}
				clsName = '';
				if (prevMonth.getMonth() < month) {
					clsName += ' old';
				} else if (prevMonth.getMonth() > month) {
					clsName += ' new';
				}
				if (prevMonth.valueOf() === currentDate) {
					clsName += ' active';
				}
				html.push('<td class="day'+clsName+'">'+prevMonth.getDate() + '</td>');
				if (prevMonth.getDay() === this.weekEnd) {
					html.push('</tr>');
				}
				prevMonth.setDate(prevMonth.getDate()+1);
			}
			this.picker.find('.datepicker-days tbody').empty().append(html.join(''));
			var currentYear = this.date.getFullYear();

			var months = this.picker.find('.datepicker-months')
						.find('th:eq(1)')
							.text(year)
							.end()
						.find('span').removeClass('active');
			if (currentYear === year) {
				months.eq(this.date.getMonth()).addClass('active');
			}

			html = '';
			year = parseInt(year/10, 10) * 10;
			var yearCont = this.picker.find('.datepicker-years')
								.find('th:eq(1)')
									.text(year + '-' + (year + 9))
									.end()
								.find('td');
			year -= 1;
			for (var i = -1; i < 11; i++) {
				html += '<span class="year'+(i === -1 || i === 10 ? ' old' : '')+(currentYear === year ? ' active' : '')+'">'+year+'</span>';
				year += 1;
			}
			yearCont.html(html);
		},

		click: function(e) {
			e.stopPropagation();
			e.preventDefault();
			var target = $(e.target).closest('span, td, th');
            var day, month, year;
			if (target.length === 1) {
				switch(target[0].nodeName.toLowerCase()) {
					case 'th':
						switch(target[0].className) {
							case 'switch':
								this.showMode(1);
								break;
							case 'prev':
							case 'next':
								this.viewDate['set'+DPGlobal.modes[this.viewMode].navFnc].call(
									this.viewDate,
									this.viewDate['get'+DPGlobal.modes[this.viewMode].navFnc].call(this.viewDate) +
									DPGlobal.modes[this.viewMode].navStep * (target[0].className === 'prev' ? -1 : 1)
								);
								this.fill();
								this.set();
								break;
						}
						break;
					case 'span':
						if (target.is('.month')) {
							month = target.parent().find('span').index(target);
							this.viewDate.setMonth(month);
						} else {
							year = parseInt(target.text(), 10)||0;
							this.viewDate.setFullYear(year);
						}
						if (this.viewMode !== 0) {
							this.date = new Date(this.viewDate);
							this.element.trigger({
								type: 'changeDate',
								date: this.date,
								viewMode: DPGlobal.modes[this.viewMode].clsName
							});
						}
						this.showMode(-1);
						this.fill();
						this.set();
						break;
					case 'td':
						if (target.is('.day')){
							day = parseInt(target.text(), 10)||1;
							month = this.viewDate.getMonth();
							if (target.is('.old')) {
								month -= 1;
							} else if (target.is('.new')) {
								month += 1;
							}
							year = this.viewDate.getFullYear();
							this.date = new Date(year, month, day,0,0,0,0);
							this.viewDate = new Date(year, month, Math.min(28, day),0,0,0,0);
							this.fill();
							this.set();
                            if (this.callback) {
			                    var formated = DPGlobal.formatDate(this.date, this.format);
                                this.callback(formated);
                            }
							this.element.trigger({
								type: 'changeDate',
								date: this.date,
								viewMode: DPGlobal.modes[this.viewMode].clsName
							});
						}
						break;
				}
			}
		},

		mousedown: function(e){
			e.stopPropagation();
			e.preventDefault();
		},

		showMode: function(dir) {
			if (dir) {
				this.viewMode = Math.max(this.minViewMode, Math.min(2, this.viewMode + dir));
			}
			this.picker.find('.datepicker>div').hide().filter('.datepicker-'+DPGlobal.modes[this.viewMode].clsName).show();
		}
	};

	var DPGlobal = {
		modes: [
			{
				clsName: 'days',
				navFnc: 'Month',
				navStep: 1
			},
			{
				clsName: 'months',
				navFnc: 'FullYear',
				navStep: 1
			},
			{
				clsName: 'years',
				navFnc: 'FullYear',
				navStep: 10
		}],
		dates:{
			days: window.WEEKDAYS,
			daysShort: window.WEEKDAYS_SHORT,
			daysMin: window.WEEKDAYS_SHORT,
			months: window.MONTHS,
			monthsShort: window.MONTHS_SHORT
		},
		isLeapYear: function (year) {
			return (((year % 4 === 0) && (year % 100 !== 0)) || (year % 400 === 0));
		},
		getDaysInMonth: function (year, month) {
			return [31, (DPGlobal.isLeapYear(year) ? 29 : 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month];
		},
		parseFormat: function(format){
			var separator = format.match(/[\-.\/\s].*?/),
				parts = format.split(/\W+/);
			if (!separator || !parts || parts.length === 0){
				throw new Error("Invalid date format.");
			}
			return {separator: separator, parts: parts};
		},
		parseDate: function(date, format) {
			var parts = date.split(format.separator),
				val;
            date = new Date();
			date.setHours(0);
			date.setMinutes(0);
			date.setSeconds(0);
			date.setMilliseconds(0);
			if (parts.length === format.parts.length) {
				for (var i=0, cnt = format.parts.length; i < cnt; i++) {
					val = parseInt(parts[i], 10)||1;
					switch(format.parts[i]) {
						case 'dd':
						case 'd':
							date.setDate(val);
							break;
						case 'mm':
						case 'm':
							date.setMonth(val - 1);
							break;
						case 'yy':
							date.setFullYear(2000 + val);
							break;
						case 'yyyy':
							date.setFullYear(val);
							break;
					}
				}
			}
			return date;
		},
		formatDate: function(date, format){
			var val = {
				d: date.getDate(),
				m: date.getMonth() + 1,
				yy: date.getFullYear().toString().substring(2),
				yyyy: date.getFullYear()
			};
			val.dd = (val.d < 10 ? '0' : '') + val.d;
			val.mm = (val.m < 10 ? '0' : '') + val.m;
			date = [];
			for (var i=0, cnt = format.parts.length; i < cnt; i++) {
				date.push(val[format.parts[i]]);
			}
			return date.join(format.separator);
		},
		headTemplate: '<thead>' +
            '<tr>' +
                '<th class="prev">&lsaquo;</th>' +
                '<th colspan="5" class="switch"></th>' +
                '<th class="next">&rsaquo;</th>' +
            '</tr>' +
        '</thead>',
		contTemplate: '<tbody><tr><td colspan="7"></td></tr></tbody>'
	};
	DPGlobal.template = '<div class="datepicker">' +
        '<div class="datepicker-days">' +
            '<table class=" table-condensed">' +
                DPGlobal.headTemplate +
                '<tbody></tbody>' +
            '</table>' +
        '</div>' +
        '<div class="datepicker-months">' +
            '<table class="table-condensed">' +
                DPGlobal.headTemplate +
                DPGlobal.contTemplate +
            '</table>' +
        '</div>' +
        '<div class="datepicker-years">' +
            '<table class="table-condensed">' +
                DPGlobal.headTemplate +
                DPGlobal.contTemplate +
            '</table>' +
        '</div>' +
    '</div>';

    var loaded = false;
    var $top_nav = $('#top_nav');
    var $mega = $('#mega_drop_down_menu');
    var key = 'mega-drop-down-menu:' + window.settings.LANGUAGE_CODE;

    function processHTML(html) {
        $mega.html(html);
        $('.calendar', $mega).each(function() {
            var $this = $(this).html(DPGlobal.template);
            var $input = $('<input type="hidden" />');
            var oDatepicker = new Datepicker($input, $this, {
                format: 'yyyy-mm-dd',
                weekStart: 1,
                callback: function(date) {
                    location.href = $this.data('url') + '?selected_date=' + date;
                }
            });
            $input.data('datepicker', oDatepicker);
            oDatepicker.show();
        });
        loaded = true;
        $top_nav.hover(function() {
            if (window.innerWidth > 767) {
                if ($('.navbar-wrapper').is('.on')) {
                    $mega.css('position', 'fixed');
                } else {
                    $mega.css('position', 'absolute');
                }
                $mega.addClass('show');
            }

        }, function() {
            $mega.removeClass('show');
            $('ul.nav>li', $top_nav).removeClass('mega-menu-active');
        });
        $('ul.nav>li', $top_nav).hover(function() {
            if (window.innerWidth > 767) {
                $('.mega_drop_down', $mega).removeClass('show');
                $('ul.nav>li', $top_nav).removeClass('mega-menu-active');
                var cssClasses = $(this).attr('class') || '';
                var m = cssClasses.match(/\bmenu-\S+/);
                if (m) {
                    if ($('#' + MAPPER[m[0]]).addClass('show').length) {
                        $(this).addClass('mega-menu-active');
                    }
                }
            }
        });
    }

    function fetchHTML() {
        $.get('/' + window.settings.LANGUAGE_CODE + '/helper/menu/', function(html) {
            processHTML(html);
            lscache.set(key, html, 10);
        }, "html");
    }

    var html = lscache.get(key);
    if (html) {
        processHTML(html);
    } else {
        fetchHTML(html);
    }

});