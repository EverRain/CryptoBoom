import { Component, Input, OnChanges, SimpleChanges, ViewChild } from '@angular/core';
import { ChartComponent, ApexNonAxisChartSeries, ApexChart, ApexPlotOptions,
         ApexFill, ApexStroke, ApexLegend, ApexResponsive } from 'ng-apexcharts';

export type ChartOptions = {
  series: ApexNonAxisChartSeries;
  chart: ApexChart;
  plotOptions: ApexPlotOptions;
  fill: ApexFill;
  stroke: ApexStroke;
  legend: ApexLegend;
  labels: string[];
  responsive: ApexResponsive[];
};

@Component({
  selector: 'app-graphcard',
  standalone: true,
  imports: [ChartComponent],
  templateUrl: './graphcard.component.html',
  styleUrls: ['./graphcard.component.scss']
})
export class GraphcardComponent implements OnChanges {
  @ViewChild('chart') chart!: ChartComponent;

  @Input() data: {
    name: string;
    nb_positif: number;
    nb_negatif: number;
    nb_neutre: number;
  }[] = [];

  public chartOptions: ChartOptions = {
    series: [0],
    chart: {
      type: 'radialBar',
      height: 300,
      sparkline: { enabled: true }
    },
    plotOptions: {
      radialBar: {
        hollow: { size: '65%' },
        track: {
          background: '#1e202f',
          strokeWidth: '100%'
        },
        dataLabels: {
          name: { show: false },
          value: {
            show: true,
            fontSize: '2rem',
            color: '#fff',
            formatter: (val) => `${val.toFixed(2)}%`
          }
        }
      }
    },
    fill: {
      type: 'gradient',
      gradient: {
        shade: 'dark',
        type: 'horizontal',
        shadeIntensity: 0.5,
        gradientToColors: ['#D946EF', '#5B21B6', '#0EA5E9'],
        inverseColors: false,
        stops: [0, 50, 100]
      }
    },
    stroke: {
      lineCap: 'round'
    },
    legend: {
      show: false
    },
    labels: [''],
    responsive: [
      {
        breakpoint: 480,
        options: {
          chart: { height: 220 }
        }
      }
    ]
  };

  ngOnChanges(changes: SimpleChanges) {
    if (this.data.length > 0) {
      const { nb_positif, nb_negatif, nb_neutre } = this.data[0];
      const total = nb_positif + nb_negatif + nb_neutre;
      const pct = total > 0 ? (nb_positif / total) * 100 : 0;
      // on met à jour la série
      this.chartOptions.series = [parseFloat(pct.toFixed(2))];
      if (this.chart) {
        this.chart.updateSeries(this.chartOptions.series);
      }
    }
  }
}
