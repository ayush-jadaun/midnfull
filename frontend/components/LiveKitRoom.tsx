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
  video = true,
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
        // Use screen pixel density to handle screens with differing densities.
        adaptiveStream: { pixelDensity: "screen" },
        // Add your existing room options
        dynacast: true,
        publishDefaults: {
          simulcast: true,
          videoSimulcastLayers: [
            {
              width: 320,
              height: 240,
              resolution: { width: 320, height: 240 },
              encoding: { maxBitrate: 150_000, maxFramerate: 15 },
            },
            {
              width: 640,
              height: 480,
              resolution: { width: 640, height: 480 },
              encoding: { maxBitrate: 500_000, maxFramerate: 30 },
            },
          ],
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
