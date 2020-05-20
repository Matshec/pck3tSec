export interface HostList {
  id: number;
  host: number;
  reason: string;
  name:string;
  time_added: Date;
}

export interface Host {
  id: number;
  fqd_name: string;
  blocked: boolean;
  original_ip: string;
  threat: boolean;
  created_at:Date;
  on_list:string;
}

export interface Threat {
  id: number;
  host_source: Host
  http_path: string;
  threat_type: string;
  threat_details: any;
  discovered: Date;

}
