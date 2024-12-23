'use client'

import { useState, useEffect } from 'react'

export default function SampleOutput() {
  const [showCursor, setShowCursor] = useState(true)

  useEffect(() => {
    const interval = setInterval(() => {
      setShowCursor((prev) => !prev)
    }, 500)
    return () => clearInterval(interval)
  }, [])

  return (
    <section className="mt-16">
      <div className="border border-green-500 rounded-lg overflow-hidden font-['IBM_Plex_Mono']">
        <div className="bg-gray-800 text-green-400 px-4 py-2 font-bold text-sm">
          <span>&gt; Story Engine: Proof of Concept</span>
        </div>
        <div className="bg-black p-6 text-green-400 text-sm leading-relaxed overflow-x-auto">
          <p className="mb-4 text-lg">&gt; Chapter 1: Scientific Discovery Gone Wrong</p>
          
          {/* Scene 1 */}
          <p className="mb-4">&gt; Location: Station Omega Lab</p>
          <p className="mb-4">&gt; Characters: Dr. James Chen</p>
          
          <div className="space-y-4 opacity-80">
            <p>
              &gt; The soft hum of quantum processors fills the dimly lit laboratory as Dr. James Chen leans closer to his holographic display, his weathered face illuminated by the pale blue light. The Fragment sample, suspended in the containment field before him, shouldn't be moving the way it is.
            </p>
            <p>
              &gt; "Run sequence delta-seven again," he mumbles to himself, fingers dancing across the haptic interface. The Fragment—a crystalline shard no larger than his thumb—pulses with an internal light that defies his understanding of its composition. According to every known law of physics, it should be inert.
            </p>
            <p>
              &gt; It isn't.
            </p>
            <p>
              &gt; The quantum readouts scroll past as Chen marks another anomaly in his research log. "Third harmonic resonance at 2300 hours. Duration: twelve seconds. Amplitude: increasing." He pauses, adjusting his wire-rimmed glasses. "Note: oscillation pattern shows signs of...optimization."
            </p>
            <p>
              &gt; The word feels wrong even as he logs it. Optimization implies purpose, intelligence. The Fragment is supposed to be a remnant of ancient technology, not an active system.
            </p>
            <p>
              &gt; A subtle shift in the containment field's pitch draws his attention. The Fragment's glow intensifies, its internal structure reorganizing in ways his instruments barely register. Chen's heart rate quickens as he initiates a full spectrum analysis. The lab's automated systems whir to life around him, bathing the Fragment in invisible fields of force and radiation.
            </p>
            <p>
              &gt; "Come on," he whispers, "show me what you're doing."
            </p>
            <p>
              &gt; The Fragment responds with a pulse of energy that sends his instruments into chaos. For a fraction of a second, Chen swears he sees patterns in the data—not random fluctuations, but something ordered, deliberate. By the time he's archived the readings, the Fragment has returned to its baseline state, leaving him with more questions than answers.
            </p>
            <p>
              &gt; He slumps in his chair, rubbing his tired eyes. The station's night cycle presses against the viewport behind him, an endless expanse of stars watching his futile efforts. After six months of study, the Fragments are still a mystery. But tonight feels different. Tonight, he's seen something new.
            </p>
            <p>
              &gt; Chen begins composing his report to Commander Drake, knowing she won't like what he has to say: The Fragments aren't just ancient artifacts. They're waking up.
            </p>

            {/* Scene 2 */}
            <p className="mt-8 mb-4">&gt; Location: Command Center</p>
            <p className="mb-4">&gt; Characters: Dr. James Chen, Commander Drake</p>
            
            <p>
              &gt; Dr. James Chen's footsteps echo through the polished corridors of Station Omega as he makes his way to the Command Center, his tablet clutched tightly against his chest. The morning's harsh fluorescent lighting does nothing to soften his features, already drawn tight with concern over the anomalous Fragment readings from the previous night.
            </p>
            <p>
              &gt; The Command Center's reinforced doors slide open with a pneumatic hiss. Inside, a dozen technicians occupy their stations, their faces bathed in the blue glow of holographic displays. Commander Drake stands at the central console, her silver-streaked hair pulled back in a regulation bun, studying a tactical overlay of the station's defensive grid.
            </p>
            <p>
              &gt; "Commander," Chen says, his voice carrying across the quiet hum of machinery. "We need to discuss the Fragment's behavior."
            </p>
            <p>
              &gt; Drake's shoulders tense slightly before she turns. "Doctor. I trust you have something concrete this time, not another theoretical model?"
            </p>
            <p>
              &gt; Chen activates his tablet, projecting a three-dimensional visualization of last night's data. Red warning indicators pulse at regular intervals. "The Fragment's quantum signature has shifted by point-three-seven percent since yesterday. It's never shown this kind of instability before."
            </p>
            <p>
              &gt; "Point-three-seven percent?" Drake's eyes narrow. "That's within standard deviation parameters."
            </p>
            <p>
              &gt; "Not for a Fragment, Commander. These artifacts have maintained quantum stability to the fifteenth decimal place since their discovery. This shift shouldn't be possible."
            </p>
            <p>
              &gt; A junior officer approaches with a security report, but Drake waves him away. She leans closer to the projection, her face illuminated by its glow. "What are the military implications?"
            </p>
            <p>
              &gt; "That's just it," Chen says, manipulating the display to show a time-lapse of the changes. "We don't know. The Fragment's containment field is holding, but these fluctuations... they're following a pattern I've never seen before. It's almost like—"
            </p>
            <p>
              &gt; "Like what, Doctor?"
            </p>
            <p>
              &gt; Chen hesitates, aware of the weight his next words will carry. "Like it's trying to communicate."
            </p>
            <p>
              &gt; Drake's expression hardens. "Or like it's preparing to breach containment. I want additional security measures in place within the hour. And I need you to focus on strengthening those containment fields, not chasing theories about alien communication."
            </p>
            <p>
              &gt; "Commander, if we miss this opportunity to understand—"
            </p>
            <p>
              &gt; "Your job is to keep that thing stable, Dr. Chen. Leave the strategic decisions to those qualified to make them." Drake turns back to her tactical display, a clear dismissal.
            </p>
            <p>
              &gt; Chen's fingers tighten around his tablet, knuckles whitening. The data continues to pulse its warning, unnoticed by everyone except him. As he turns to leave, the Fragment's quantum signature shifts again, this time by point-three-eight percent.
            </p>
            <p className="flex mt-4">
              <span>&gt;&nbsp;</span>
              <span className={showCursor ? 'opacity-100' : 'opacity-0'}>▋</span>
            </p>
          </div>
        </div>
      </div>
    </section>
  )
} 