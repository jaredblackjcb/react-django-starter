/* tslint:disable */
/* eslint-disable */
/**
 * Starter App
 * A starter project with a server-rendered SPA architecture.
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface AggregateEmployeeData
 */
export interface AggregateEmployeeData {
    /**
     * 
     * @type {{ [key: string]: any; }}
     * @memberof AggregateEmployeeData
     */
    totalCosts: { [key: string]: any; };
    /**
     * 
     * @type {{ [key: string]: any; }}
     * @memberof AggregateEmployeeData
     */
    averageSalaries: { [key: string]: any; };
    /**
     * 
     * @type {{ [key: string]: any; }}
     * @memberof AggregateEmployeeData
     */
    headcounts: { [key: string]: any; };
}

/**
 * Check if a given object implements the AggregateEmployeeData interface.
 */
export function instanceOfAggregateEmployeeData(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "totalCosts" in value;
    isInstance = isInstance && "averageSalaries" in value;
    isInstance = isInstance && "headcounts" in value;

    return isInstance;
}

export function AggregateEmployeeDataFromJSON(json: any): AggregateEmployeeData {
    return AggregateEmployeeDataFromJSONTyped(json, false);
}

export function AggregateEmployeeDataFromJSONTyped(json: any, ignoreDiscriminator: boolean): AggregateEmployeeData {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'totalCosts': json['total_costs'],
        'averageSalaries': json['average_salaries'],
        'headcounts': json['headcounts'],
    };
}

export function AggregateEmployeeDataToJSON(value?: AggregateEmployeeData | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'total_costs': value.totalCosts,
        'average_salaries': value.averageSalaries,
        'headcounts': value.headcounts,
    };
}

