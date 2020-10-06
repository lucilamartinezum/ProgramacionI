import { Component, OnInit } from '@angular/core';
import  {Sensor} from "./sensor.model"

@Component({
  selector: 'app-sensor',
  templateUrl: './sensor.component.html',
  styleUrls: ['./sensor.component.scss']
})
export class SensorComponent implements OnInit {
  selectedSensor: Sensor;
  sensors: Sensor[]=[
    {
      name: 'Pablo',
      active: true,
      status: true,
      id_num : 1,
    },
    {
      name: 'Mica',
      active: true,
      status: true,
      id_num : 2,
    },
  {
      name: "Ivan",
      active: true,
      status: false,
      id_num : 3,
    },
    {
      name: 'Lu',
      active: true,
      status: true,
      id_num : 5,
    },
    {
      name: 'Fede',
      active: false,
      status: true,
      id_num : 4,
    },
   
  ];
  constructor() { }

  ngOnInit(): void {
  }
  onSelect(sensor:Sensor): void{
    this.selectedSensor=sensor;
  }
}
