import { Routes } from '@angular/router';
import { ArticlesComponent } from './pages/articles/articles.component';
import { HomeComponent } from './pages/home/home.component';

export const routes: Routes = [
  { path: '', component: HomeComponent},
  { path: 'articles', component: ArticlesComponent },
];