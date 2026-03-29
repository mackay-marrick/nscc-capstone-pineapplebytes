<<<<<<< HEAD
﻿export interface SystemTicket {
=======
export interface SystemTicket {
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49
  system: string;
  openTickets: number;
  resolved: number;
  healthStatus: 'Critical' | 'Warning' | 'Healthy';
}

export interface TicketVolumeData {
  id: string;
  month: string;
  count: number;
}

export interface SystemFailure {
  system: string;
  issue: string;
  impact: 'High' | 'Medium' | 'Low';
}

export interface RiskNote {
  title: string;
  description: string;
  severity: 'High' | 'Medium' | 'Low';
}

export interface Restaurant {
  id: string;
  name: string;
  location: string;
  generalManager: string;
  regionTier: string;
  reportingPeriod: string;
  
  // Core Systems Health
  halCertHealth: number;
  miamiBoardHealth: number;
  coreSystemsOverall: number;
  networkInfrastructure: number;
  
  // Support Tickets
  systemTickets: SystemTicket[];
  ticketVolumeHistory: TicketVolumeData[];
  totalTicketsLast90Days: number;
  
  // System Failures
  recurringFailures: SystemFailure[];
  
  // Risk Notes
  operationalRisks: RiskNote[];
  
  // AI Overview
  executiveSummary: string;
  networkInfrastructureNotes: string;
  hardwareDegradation: string;
  staffTrainingGaps: string;
  
  // Recommendations
  recommendations: {
    technical: string[];
    operational: string[];
  };
  
  // Operational Metrics
  totalTickets: number;
  criticalIncidents: number;
  avgResponseTime: number;
  systemUptime: number;
  caseResponseVerified: boolean;
}

export const mockRestaurants: Restaurant[] = [
  {
    id: '1',
    name: 'The Grill House - Halifax',
    location: 'Halifax, NS',
    generalManager: 'Marcus Sterling',
    regionTier: 'Atlantic Tier 1',
    reportingPeriod: 'Last 90 Days (Late 2024 - Mar 2025)',
    
    halCertHealth: 98.4,
    miamiBoardHealth: 92.6,
    coreSystemsOverall: 88.2,
    networkInfrastructure: 94.1,
    
    systemTickets: [
      { system: 'POS Systems', openTickets: 2, resolved: 12, healthStatus: 'Healthy' },
      { system: 'Kitchen Display', openTickets: 1, resolved: 8, healthStatus: 'Healthy' },
      { system: 'Online Orders', openTickets: 0, resolved: 15, healthStatus: 'Healthy' },
      { system: 'WiFi Network', openTickets: 3, resolved: 6, healthStatus: 'Warning' },
      { system: 'Payment Terminal', openTickets: 0, resolved: 9, healthStatus: 'Healthy' },
    ],
    
    ticketVolumeHistory: [
      { id: 'hfx-oct', month: 'Oct', count: 8 },
      { id: 'hfx-nov', month: 'Nov', count: 12 },
      { id: 'hfx-dec', month: 'Dec', count: 18 },
      { id: 'hfx-jan', month: 'Jan', count: 15 },
      { id: 'hfx-feb', month: 'Feb', count: 10 },
      { id: 'hfx-mar', month: 'Mar', count: 7 },
    ],
    
    totalTicketsLast90Days: 154,
    
    recurringFailures: [
      { 
        system: 'POS Terminal', 
        issue: 'Random freezing during shift', 
        impact: 'High' 
      },
      { 
        system: 'WiFi Router', 
        issue: 'Power cutout causing intermittent loss', 
        impact: 'Medium' 
      },
      { 
        system: 'Receipt Printer', 
        issue: 'Paper jam (~3 times per day)', 
        impact: 'Low' 
      },
    ],
    
    operationalRisks: [
      {
        title: 'Terminal Leakage: Offline Mode Stuck',
        description: 'One POS terminal at this location is occasionally stuck in offline mode. This may indicate a faulty network adapter or intermittent power supply issue. Recommend on-site inspection to isolate or swap this terminal.',
        severity: 'High'
      },
      {
        title: 'WiFi Latency in the East Zone',
        description: 'Multiple reports are coming in from the east-seating location, where tablets are failing to sync properly. The service latency has been higher than in other zones. May require reboot or physical inspection of the access point.',
        severity: 'Medium'
      },
    ],
    
    executiveSummary: 'Despite current performance at The Grill House - Halifax, servers within acceptable thresholds, longer-period trending shows slower service times during peak dinner hours.',
    
<<<<<<< HEAD
    networkInfrastructureNotes: 'The primary network has identified nine recent occurrence events (detailed network disruption events) over the POS router and location gateway. While all outages (Γëñ 60s) on the network timeline are concerning past the threshold, specifically once the failure point.',
=======
    networkInfrastructureNotes: 'The primary network has identified nine recent occurrence events (detailed network disruption events) over the POS router and location gateway. While all outages (≤ 60s) on the network timeline are concerning past the threshold, specifically once the failure point.',
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49
    
    hardwareDegradation: 'We have observed a trend in the thermal printing of the front-of-house terminals. Terminal 03 is showing signs of hardware aging, specifically low capacity issues with buffering to the required peak performance.',
    
    staffTrainingGaps: 'Recent observations indicate intermittent user errors with the new POS system. Staff is experiencing a moderate learning curve with the "Weekend Rush" scheduling screen for inventory sign-off at the end of the Sunday lunch or immediately a more robust stage scheduling practice.',
    
    recommendations: {
      technical: [
        'CONNECTIVITY: Add 24/7 backup AP',
        'Deploy Ethernet at 5 POs (if Wifi at least fixed later)',
        'Replace POS Terminal on 03 Aug (est valid till week)',
        'Enable Network Segmentation for SuperWiFi 6E',
      ],
      operational: [
        'OPERATIONAL REQUIREMENTS: 3',
        'Implement weekly financial clearing for WIFI card',
        'Staff daily resolution on 04 Aug (EST AM shift)',
        'Upgrade "Rush" support list for Weekend - for quality fields',
      ],
    },
    
    totalTickets: 38,
    criticalIncidents: 0,
    avgResponseTime: 1.4,
    systemUptime: 98.2,
    caseResponseVerified: true,
  },
  {
    id: '2',
    name: 'Oceanside Bistro - Vancouver',
    location: 'Vancouver, BC',
    generalManager: 'Sarah Chen',
    regionTier: 'Pacific Tier 1',
    reportingPeriod: 'Last 90 Days (Late 2024 - Mar 2025)',
    
    halCertHealth: 95.8,
    miamiBoardHealth: 89.3,
    coreSystemsOverall: 91.5,
    networkInfrastructure: 96.7,
    
    systemTickets: [
      { system: 'POS Systems', openTickets: 1, resolved: 15, healthStatus: 'Healthy' },
      { system: 'Kitchen Display', openTickets: 0, resolved: 10, healthStatus: 'Healthy' },
      { system: 'Online Orders', openTickets: 2, resolved: 18, healthStatus: 'Warning' },
      { system: 'WiFi Network', openTickets: 0, resolved: 8, healthStatus: 'Healthy' },
      { system: 'Payment Terminal', openTickets: 1, resolved: 12, healthStatus: 'Healthy' },
    ],
    
    ticketVolumeHistory: [
      { id: 'van-oct', month: 'Oct', count: 10 },
      { id: 'van-nov', month: 'Nov', count: 14 },
      { id: 'van-dec', month: 'Dec', count: 20 },
      { id: 'van-jan', month: 'Jan', count: 18 },
      { id: 'van-feb', month: 'Feb', count: 12 },
      { id: 'van-mar', month: 'Mar', count: 9 },
    ],
    
    totalTicketsLast90Days: 176,
    
    recurringFailures: [
      { 
        system: 'Online Orders', 
        issue: 'Integration timeout with delivery apps', 
        impact: 'High' 
      },
      { 
        system: 'Kitchen Display', 
        issue: 'Screen brightness fluctuation', 
        impact: 'Low' 
      },
    ],
    
    operationalRisks: [
      {
        title: 'Third-Party Integration Delays',
        description: 'Online ordering system occasionally experiences delays when communicating with third-party delivery platforms. This impacts order accuracy and customer satisfaction during peak hours.',
        severity: 'Medium'
      },
    ],
    
    executiveSummary: 'Oceanside Bistro maintains strong operational performance with excellent network reliability. The primary focus area is optimizing third-party delivery integrations during high-traffic periods.',
    
    networkInfrastructureNotes: 'Network infrastructure is robust with redundant systems in place. Recent upgrade to WiFi 6 has improved connectivity across all zones.',
    
    hardwareDegradation: 'All hardware is within acceptable performance ranges. Scheduled replacement of kitchen display screens planned for Q3 2025.',
    
    staffTrainingGaps: 'Staff demonstrates high proficiency with current systems. Recommend refresher training on new online ordering features.',
    
    recommendations: {
      technical: [
        'INTEGRATION: Optimize API timeout settings',
        'Add redundant delivery platform connection',
        'Upgrade kitchen display units in Q3',
        'Implement load balancing for peak hours',
      ],
      operational: [
        'TRAINING REQUIREMENTS: 2',
        'Conduct monthly system efficiency reviews',
        'Create escalation protocol for delivery issues',
        'Implement customer communication templates',
      ],
    },
    
    totalTickets: 42,
    criticalIncidents: 1,
    avgResponseTime: 1.8,
    systemUptime: 99.1,
    caseResponseVerified: true,
  },
  {
    id: '3',
    name: 'Downtown Diner - Toronto',
    location: 'Toronto, ON',
    generalManager: 'James Mitchell',
    regionTier: 'Central Tier 2',
    reportingPeriod: 'Last 90 Days (Late 2024 - Mar 2025)',
    
    halCertHealth: 91.2,
    miamiBoardHealth: 87.8,
    coreSystemsOverall: 85.6,
    networkInfrastructure: 89.4,
    
    systemTickets: [
      { system: 'POS Systems', openTickets: 4, resolved: 10, healthStatus: 'Warning' },
      { system: 'Kitchen Display', openTickets: 2, resolved: 7, healthStatus: 'Warning' },
      { system: 'Online Orders', openTickets: 1, resolved: 11, healthStatus: 'Healthy' },
      { system: 'WiFi Network', openTickets: 5, resolved: 4, healthStatus: 'Critical' },
      { system: 'Payment Terminal', openTickets: 2, resolved: 6, healthStatus: 'Warning' },
    ],
    
    ticketVolumeHistory: [
      { id: 'tor-oct', month: 'Oct', count: 12 },
      { id: 'tor-nov', month: 'Nov', count: 16 },
      { id: 'tor-dec', month: 'Dec', count: 22 },
      { id: 'tor-jan', month: 'Jan', count: 25 },
      { id: 'tor-feb', month: 'Feb', count: 18 },
      { id: 'tor-mar', month: 'Mar', count: 14 },
    ],
    
    totalTicketsLast90Days: 198,
    
    recurringFailures: [
      { 
        system: 'WiFi Network', 
        issue: 'Frequent disconnections during peak hours', 
        impact: 'High' 
      },
      { 
        system: 'POS Terminal', 
        issue: 'Card reader malfunction', 
        impact: 'High' 
      },
      { 
        system: 'Kitchen Display', 
        issue: 'Order queue not updating in real-time', 
        impact: 'Medium' 
      },
    ],
    
    operationalRisks: [
      {
        title: 'Network Infrastructure Overload',
        description: 'High-traffic location experiencing significant network strain during lunch and dinner rushes. Multiple access points showing degraded performance. Urgent infrastructure upgrade recommended.',
        severity: 'High'
      },
      {
        title: 'POS Hardware End-of-Life',
        description: 'Several POS terminals are approaching end-of-life status. Increased failure rate observed over the past 60 days. Replacement plan should be accelerated.',
        severity: 'High'
      },
    ],
    
    executiveSummary: 'Downtown Diner - Toronto is experiencing elevated technical issues due to high customer volume and aging infrastructure. Immediate attention required for network and POS hardware upgrades.',
    
    networkInfrastructureNotes: 'Current network capacity is insufficient for peak demand. Multiple WiFi dead zones identified. Recommendation: Complete network redesign with enterprise-grade equipment.',
    
    hardwareDegradation: 'Critical hardware aging detected across multiple systems. POS terminals 1, 3, and 5 showing signs of hardware failure. Kitchen display units experiencing intermittent power issues.',
    
    staffTrainingGaps: 'Staff reports frustration with system reliability issues. Additional training needed on backup procedures and manual order processing during system outages.',
    
    recommendations: {
      technical: [
        'URGENT: Complete network infrastructure overhaul',
        'Replace 3 POS terminals within 30 days',
        'Install backup power for critical systems',
        'Upgrade to mesh WiFi network topology',
        'Deploy network monitoring and alerting',
      ],
      operational: [
        'CRITICAL REQUIREMENTS: 5',
        'Develop comprehensive business continuity plan',
        'Train staff on emergency manual procedures',
        'Implement daily system health checks',
        'Schedule weekly technical review meetings',
      ],
    },
    
    totalTickets: 56,
    criticalIncidents: 3,
    avgResponseTime: 2.8,
    systemUptime: 94.3,
    caseResponseVerified: false,
  },
<<<<<<< HEAD
];
=======
];
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49
