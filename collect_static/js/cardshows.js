import ReactDOM from 'react-dom'

var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function (t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var dates = [
    {
        day: 30,
        full: "2022-01-30"
    },
    {
        day: 31,
        full: "2022-01-31"
    },
    {
        day: 1,
        full: "2022-02-01",
        title: "Dark Chocolate Day"
    }, {
        day: 2,
        full: "2022-02-02",
        title: "Groundhog Day"
    }, {
        day: 3,
        full: "2022-02-03",
        title: "Carrot Cake Day"
    }, {
        day: 4,
        full: "2022-02-04",
        title: "Wear Red Day"
    }, {
        day: 5,
        full: "2022-02-05",
        title: "Weatherperson's Day"
    }, {
        day: 6,
        full: "2022-02-06",
        title: "Chopsticks Day"
    }, {
        day: 7,
        full: "2022-02-07",
        title: "Periodic Table Day"
    }, {
        day: 8,
        full: "2022-02-08",
        title: "Kite Flying Day"
    }, {
        day: 9,
        full: "2022-02-09",
        title: "Pizza Day"
    }, {
        day: 10,
        full: "2022-02-10",
        title: "Umbrella Day"
    }, {
        day: 11,
        full: "2022-02-11",
        title: "Inventor's Day"
    }, {
        day: 12,
        full: "2022-02-12",
        title: "Global Movie Day"
    }, {
        day: 13,
        full: "2022-02-13",
        title: "Tortellini Day"
    }, {
        day: 14,
        full: "2022-02-14",
        title: "Valentine's Day"
    }, {
        day: 15,
        full: "2022-02-15",
        title: "Gumdrop Day"
    }, {
        day: 16,
        full: "2022-02-16",
        title: "Do a Grouch a Favor Day"
    }, {
        day: 17,
        full: "2022-02-17",
        title: "Cabbage Day"
    }, {
        day: 18,
        full: "2022-02-18",
        title: "Battery Day"
    }, {
        day: 19,
        full: "2022-02-19",
        title: "Chocolate Mint Day"
    }, {
        day: 20,
        full: "2022-02-20",
        title: "Love Your Pet Day"
    }, {
        day: 21,
        full: "2022-02-21",
        title: "President's Day"
    }, {
        day: 22,
        full: "2022-02-22",
        title: "Cook a Sweet Potato Day"
    }, {
        day: 23,
        full: "2022-02-23",
        title: "Tile Day"
    }, {
        day: 24,
        full: "2022-02-24",
        title: "Toast Day"
    }, {
        day: 25,
        full: "2022-02-25",
        title: "Clam Chowder Day"
    }, {
        day: 26,
        full: "2022-02-26",
        title: "Pistachio Day"
    }, {
        day: 27,
        full: "2022-02-27",
        title: "Polar Bear Day"
    }, {
        day: 28,
        full: "2022-02-28",
        title: "Tooth Fairy Day"
    },
    {
        day: 1,
        full: "2022-03-01"
    }, {
        day: 2,
        full: "2022-03-02"
    }, {
        day: 3,
        full: "2022-03-03"
    }, {
        day: 4,
        full: "2022-03-04"
    }, {
        day: 5,
        full: "2022-03-05"
    }
].map(function (date, index) {
    return (__assign(__assign({}, date), {index: index}));
});
var weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
];
var DateUtility = {
    getAllDates: function () {
        return dates;
    },
    getDayOfWeek: function (day) {
        return DateUtility.getWeekdays()[day];
    },
    getWeekdays: function () {
        return weekdays;
    }
};
var TransformUtility = {
    calculateX: function (index, calendarWidth, boxSize, scale, gridGap) {
        var startingColumnIndex = 3, startingXPercent = -50;
        var columnIndex = index % 7, columnIndexDiff = columnIndex - startingColumnIndex;
        var xPaddingPercent = ((gridGap * columnIndexDiff) / calendarWidth) * 100,
            xWidthPercent = ((columnIndexDiff * boxSize) / calendarWidth) * 100,
            xPercent = xPaddingPercent + xWidthPercent;
        return startingXPercent - (xPercent * scale);
    },
    calculateY: function (index, calendarHeight, boxSize, scale, gridGap) {
        var startingRowIndex = 2, startingYPercent = -50;
        var rowIndex = Math.floor(index / 7), rowIndexDiff = rowIndex - startingRowIndex;
        var yPaddingPercent = ((gridGap * rowIndexDiff) / calendarHeight) * 100,
            yHeightPercent = ((rowIndexDiff * boxSize) / calendarHeight) * 100,
            yPercent = yPaddingPercent + yHeightPercent;
        return startingYPercent - (yPercent * scale);
    },
    getGridGap: function () {
        var calendar = document.getElementById("calendar-dates");
        if (calendar) {
            var style = window.getComputedStyle(calendar);
            return style.getPropertyValue("gap");
        }
    }
};
var DateBox = function (props) {
    var today = new Date("2022-02-01T12:00:00"), date = new Date("".concat(props.full, "T12:00:00"));
    var activeMonth = today.getMonth() === date.getMonth(),
        activeDay = activeMonth && today.getDate() === date.getDate();
    var getTitle = function () {
        if (props.title) {
            return ('<div className="date-title"><div className="date-title-dot"/><h2>{props.title}</h2></div>');
        }
    };
    var getActiveDayIndicator = function () {
        if (activeDay) {
            return ('<div className="active-day-indicator"/>');
        }
    };
    var getClasses = function () {
        return classNames("date-wrapper", {
            "active-day": activeDay,
            "active-month": activeMonth
        });
    };
    var id = "date-".concat(props.full);
    return ('<button id={id} className={getClasses()} disabled={!activeMonth} onClick={props.select}><div className="date"><div className="date-day"><h2 className="date-day-of-month">{date.getDate()}</h2><h2 className="date-day-of-week">{DateUtility.getDayOfWeek(date.getDay()).substring(0, 3)}</h2></div>{getTitle()}</div>{getActiveDayIndicator()}</button>');
};
var Calendar = function () {
    var _a = React.useState({
        boxSize: null,
        calendarSize: null,
        selectedDate: null,
        windowSize: null
    }), state = _a[0], setStateTo = _a[1];
    var ref = React.useRef(null);
    var setBoxSizeTo = function (boxSize) {
        setStateTo(__assign(__assign({}, state), {boxSize: boxSize}));
    };
    var setCalendarSizeTo = function (calendarSize) {
        setStateTo(__assign(__assign({}, state), {calendarSize: calendarSize}));
    };
    var setSelectedDateTo = function (selectedDate) {
        setStateTo(__assign(__assign({}, state), {selectedDate: selectedDate}));
    };
    React.useEffect(function () {
        if (ref) {
            var box = document.getElementById("date-2022-02-01");
            var boxSize = {
                height: box.clientHeight,
                width: box.clientWidth
            };
            var calendarSize = {
                height: ref.current.clientHeight,
                width: ref.current.clientWidth
            };
            setStateTo(__assign(__assign({}, state), {boxSize: boxSize, calendarSize: calendarSize}));
        }
    }, [state.windowSize]);
    React.useEffect(function () {
        var handleOnResize = function () {
            var windowSize = {
                height: window.innerHeight,
                width: window.innerWidth
            };
            setStateTo(__assign(__assign({}, state), {selectedDate: null, windowSize: windowSize}));
        };
        handleOnResize();
        window.addEventListener("resize", handleOnResize);
        return function () {
            window.removeEventListener("resize", handleOnResize);
        };
    }, []);
    var selectDate = function (date) {
        if (state.windowSize && state.windowSize.width > 1000) {
            if (state.selectedDate && state.selectedDate.full === date.full) {
                setSelectedDateTo(null);
            } else {
                setSelectedDateTo(date);
            }
        }
    };
    var getDates = function () {
        return dates.map(function (date) {
            return ('<DateBox key={date.full} day={date.day} full={date.full} title={date.title}selected={state.selectedDate && state.selectedDate.full === date.full} select={function () {return selectDate(date);}}/>');
        });
    };
    var getStyles = function () {
        var styles = {};
        var calendarSize = state.calendarSize, boxSize = state.boxSize, selectedDate = state.selectedDate;
        if (calendarSize && boxSize && selectedDate) {
            var scale = 4, gridGap = parseInt(TransformUtility.getGridGap());
            var x = TransformUtility.calculateX(selectedDate.index, calendarSize.width, boxSize.width, scale, gridGap),
                y = TransformUtility.calculateY(selectedDate.index, calendarSize.height, boxSize.height, scale, gridGap);
            styles.transform = "translate(".concat(x, "%, ").concat(y, "%) scale(").concat(scale, ")");
        }
        return styles;
    };
    return ('<div id="calendar"><div ref={ref} id="calendar-dates" style={getStyles()}> {getDates()}</div></div>');
};
var Background = function () {
    return ('<div id="calendar-background-wrapper"><div id="calendar-background"/></div>');
};
var App = function () {
    return ('<div id="app"><Background/><Calendar/></div>');
};
ReactDOM.render(App, document.getElementById("root"));
