import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GraphcardComponent } from '../../components/cards/graphcard/graphcard.component';
// import { GraphcardComponent } from '../components/cards/graphcard.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, GraphcardComponent],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  graphData = [
    {
      name: 'Bitcoin',
      nb_positif: 3,
      nb_negatif: 2,
      nb_neutre: 3,
      average: 33.33 // 👈 un `number` et non une `string`
    },{
      name: 'Bitcoin',
      nb_positif: 3,
      nb_negatif: 2,
      nb_neutre: 3,
      average: 33.33 // 👈 un `number` et non une `string`
    },{
      name: 'Bitcoin',
      nb_positif: 3,
      nb_negatif: 2,
      nb_neutre: 3,
      average: 33.33 // 👈 un `number` et non une `string`
    },{
      name: 'Bitcoin',
      nb_positif: 3,
      nb_negatif: 2,
      nb_neutre: 3,
      average: 33.33 // 👈 un `number` et non une `string`
    },{
      name: 'Bitcoin',
      nb_positif: 3,
      nb_negatif: 2,
      nb_neutre: 3,
      average: 33.33 // 👈 un `number` et non une `string`
    },{
      name: 'Bitcoin',
      nb_positif: 3,
      nb_negatif: 2,
      nb_neutre: 3,
      average: 33.33 // 👈 un `number` et non une `string`
    },{
      name: 'Bitcoin',
      nb_positif: 3,
      nb_negatif: 2,
      nb_neutre: 3,
      average: 33.33 // 👈 un `number` et non une `string`
    },
  ];
}