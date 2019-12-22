function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

class MyChart {

    constructor(where, symbol) {
        this.where = where;
        this.config_dict = {
            width: where.offsetWidth,
            height: window.innerHeight * 0.5,
            crosshair: {
                mode: LightweightCharts.CrosshairMode.Normal
            },
            localization: {
                dateFormat: 'yy/MM/dd',
            },
        };
        this.chart;
        this.series;
        this.symbol = symbol;
    };

    addChart(data) {
        const chart = LightweightCharts.createChart(this.where, this.config_dict);
        const series = chart.addCandlestickSeries();
        series.setData(data);
        this.chart = chart;
        this.series = series;
        this.addTooltip(80, 80, 15);
        return this;
    };

    updateSize() {
        this.chart.resize(window.innerHeight * 0.5, this.where.offsetWidth);
    };

    getChart() {
        return this.chart;
    };

    getSeries() {
        return this.series;
    };

    getSymbol() {
        return this.symbol;
    }

    setInvert() {
        this.chart.applyOptions({
            priceScale: {
                invertScale: !this.chart.options().priceScale.invertScale,
            },
        }, );
    }

    dateToString(businessDay) {
        return businessDay['year'] + '-' + businessDay['month'] + '-' + businessDay['day'];
    }

    addTooltip(w, h, m) {
        var toolTipWidth = w;
        var toolTipHeight = h;
        var toolTipMargin = m;

        var container = document.createElement('div');
        this.where.appendChild(container);

        var toolTip = document.createElement('div');
        toolTip.className = 'floating-tooltip';
        container.appendChild(toolTip);

        var object_ = this;
        this.chart.subscribeCrosshairMove(function (param) {

            if (param.point === undefined || !param.time) {
                toolTip.style.display = 'None';
                return;
            } else {
                const dateStr = object_.dateToString(param.time);
                toolTip.style.display = 'block';
                var price = param.seriesPrices.values().next().value;
                toolTip.innerHTML = '<div style="color: #009688;font-size: 18px;">' +
                    object_.symbol + '</div><div style="font-size: 14px; margin: 4px 0px; color: #21384d">' + '시가:' + numberWithCommas(price.open) +
                    '</div><div style="font-size: 14px; margin: 4px 0px; color: #21384d">' + '종가:' + numberWithCommas(price.close) +
                    '</div><div style="color: #21384d">' + dateStr + '</div>';

                var coordinate = object_.series.priceToCoordinate(price);
                var shiftedCoordinate = param.point.x - 50;
                if (coordinate === null) {
                    return;
                }
                shiftedCoordinate = Math.max(0, Math.min(container.clientWidth - toolTipWidth, shiftedCoordinate));
                var coordinateY = coordinate - toolTipHeight - toolTipMargin > 0 ? coordinate - toolTipHeight - toolTipMargin : Math.max(0, Math.min(container.clientHeight - toolTipHeight - toolTipMargin, coordinate + toolTipMargin));
                toolTip.style.left = shiftedCoordinate + 'px';
                toolTip.style.top = coordinateY + 'px';
            }
        });
    };
}