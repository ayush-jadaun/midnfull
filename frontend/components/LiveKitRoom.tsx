import React from "react";
import { View, StyleSheet } from "react-native";
import {
  LiveKitRoom as LiveKitRoomNative,
  AudioSession,
} from "@livekit/react-native";
import { useEffect } from "react";

interface LiveKitRoomProps {
  children: React.ReactNode;
  token: string;
  serverUrl: string;
  onConnected?: () => void;
  onDisconnected?: () => void;
  audio?: boolean;
  video?: boolean;
  connect?: boolean;
}

export function LiveKitRoom({
  children,
  token,
  serverUrl,
  onConnected,
  onDisconnected,
  audio = true,
  video = false, // Default to audio-only
  connect = true,
}: LiveKitRoomProps) {
  // Start the audio session first - following the docs pattern
  useEffect(() => {
    let start = async () => {
      await AudioSession.startAudioSession();
    };
    start();
    return () => {
      AudioSession.stopAudioSession();
    };
  }, []);

  return (
    <LiveKitRoomNative
      serverUrl={serverUrl}
      token={token}
      connect={connect}
      options={{
        // Optimized for audio-only calls
        adaptiveStream: false, 
        dynacast: true,
        publishDefaults: {
          simulcast: false,

          audioPreset: {
            maxBitrate: 64_000, 
          },
        },
      }}
      audio={audio}
      video={video}
      onConnected={onConnected}
      onDisconnected={onDisconnected}
    >
      <View style={styles.container}>{children}</View>
    </LiveKitRoomNative>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
