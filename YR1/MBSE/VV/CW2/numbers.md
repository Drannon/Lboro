# Numbers for performance requirements

x = Forwards Acceleration = 2 m/s  
y = Extreme Forwards Acceleration 1 m/s 
z = Top Speed through Water 12 kts  
a = Astern Acceleration = 1 m/s  
b = Extreme Astern Acceleration 0.5 m/s    
c = Turn Circle  
d = Rudder Return  
e = Maximum Turning Rate  
f = Endurance  
g = Exreme Endurance  
h = Charging Speed >= 2 h  
i = Normal Temeperature Low  
j = Normal Temeperature High  
k = Extreme Temperature Low  
l = Extreme Temperature High  
m = Number of Cars   
n = Number of Passengers  
o = Maximum Draught = 1.1m  
p = Maximum Displacement  
q = Maximum Length  
r = Maximum Beam  
s = Maximum Height  
t = Emergency Stop Response Time  
u = Paying Rate  
v = Lateral Speed  

---

## Propulsion

*x, y, z, a, b, c, d, e, v*

- ISO 19019 recommends a torsion guage installed for propulsion system >= 2 MW
- => 1,999 MW power
- Karekla *et al.* determine an acceleration of $1 m/s^2$ reasonable for a bus, so adopt for ferry.
- Jerk is the important thing here along with acceleration, but this is without scope. future work?
- Acceleration MAY be too great a challenge

- Speed ~ 10 kts
- Some random source says that the ferry has two 500hp diesel engines, so 1 MW would exceed the ferry's performance
- Assume a top speed 20% greater than cruise, therefore 12 kts top speed
- 1 MW motor still unobtainium, so 2 500kw motors taking the assumption that this is equivalent. It's not because of multi-shaft efficiencies etc.
- Motors are reversable and not geared, so assume astern propulsion is around 50% as efficient as forward propulsion. This is likely not true.
- Find motor performance against temperature.
- Must consider drag here, we'll ignore most of it but stick to $\frac{1}{2} \rho u^{2} S C_{D}$ with $S$ calculated using the method in whatever that paper was.

## Battery

*f, h, i, j, k, l*

1 mWh battery would (assumedly) provide 1 hour of operation for motor operating at 1 MW.  
This is potentially suitable, and this could be scaled to extend.
1 MWh batteries are available.
They are however expensive.
Charging time also possibly an issue - Though electric vehicles are capable of 400 kw, which would then result in a 2 hour charging time to 80%.

## Draught and Displacement

*m, n, o, p, q, r, s*

I think these are nice to haves, with the time available this may be too much. Assuming a draught of 1m to keep it consistent. Maybe back up with thames charts
Sizing based on standard vehicles, strong maybe on hull profile.
OSINT for capacity based on deck area, then extrapolate for passenger figures

## Comms

*t*

## Other

*u*

---

## Notes

> I'm thinking of just ignoring *t* and *u*, because that's just lame.
> I'd like to runs sims for endurance, top speed, acceleration, MAYBE turning.
> Not bothered about lateral movement etc.
> Analysis on Cargo is idea as it should be static, will need a hull profile though.
