import React from "react";
import { LiveKitRoom } from "./LiveKitRoom";

interface LiveKitProviderProps {
  children: React.ReactNode;
  token: string;
  url: string;
  audio?: boolean;
  video?: boolean;
  onConnected?: () => void;
  onDisconnected?: () => void;
}

export function LiveKitProvider({
  children,
  token,
  url,
  audio = true,
  video = false, 
  onConnected,
  onDisconnected,
}: LiveKitProviderProps) {
  return (
    <LiveKitRoom
      token={token}
      serverUrl={url}
      connect={true}
      audio={audio}
      video={video}
      onConnected={onConnected}
      onDisconnected={onDisconnected}
    >
      {children}
    </LiveKitRoom>
  );
}
