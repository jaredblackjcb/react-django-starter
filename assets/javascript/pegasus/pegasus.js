import {getApiConfiguration} from "../api";
import {PegasusApi} from "../api-client";

export { Charts } from './examples/charts';

export function getPegasusApiClient(serverBaseUrl) {
  return new PegasusApi(getApiConfiguration(serverBaseUrl));
}
